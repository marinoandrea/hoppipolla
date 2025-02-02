use std::{
    borrow::Cow,
    collections::{HashMap, HashSet},
    hash::Hash,
};

use clingo::{control, ClingoError, FactBase, Part, Symbol};

use crate::entities::{Issuer, MetaPolicy, Policy, PolicyId, DEFAULT_ISSUER};
use crate::policy_manager as pb;

const SYMBOL_SRC: &str = "src";
const SYMBOL_DST: &str = "dst";
const SYMBOL_LINK: &str = "link";
const SYMBOL_CHOSEN: &str = "chosen";
const SYMBOL_ISSUED: &str = "issued";
const SYMBOL_POWER: &str = "power";
const SYMBOL_CONFLICTING: &str = "conflicting";
const SYMBOL_DEACTIVATE: &str = "deactivate";

const PROBLEM_ENCODING: &str = "
{ chosen(X, XIF, Y, YIF) : link(X, XIF, Y, YIF) } 1 :- link(X, _, _, _).

% check inclusion of source and destination
:- src(S), not chosen(S, _, _, _).
:- dst(D), not chosen(_, _, D, _).

% check continuity
:- chosen(_, _, Y, YIF), #count { X, XIF : chosen(X, XIF, Y, YIF) } != 1, not src(Y).
:- chosen(X, XIF, _, _), #count { Y, YIF : chosen(X, XIF, Y, YIF) } != 1, not dst(X).

% check reachability
reachable(S) :- src(S).
reachable(Y) :- reachable(X), chosen(X, _, Y, _).
:- dst(D), not reachable(D).

% filter out empty models
:- #count { : chosen(_, _, _, _) } == 0.

#show chosen/4.
";

const META_PROBLEM_ENCODING: &str = "
conflicting(P2, P1) :- conflicting(P1, P2).

:- conflicting(P1, P2), 
    not overrides(_, P2), 
    not overrides(_, P1).

deactivate(P) :- overrides(_, P).

% filter out empty models
:- #count { : deactivate(_) } == 0, #count { : conflicting(_, _) } > 0.

#show deactivate/1.
";

pub fn solve(
    pi: &ProblemInstance,
    policies: Vec<Policy>,
    issuers: Vec<Issuer>,
    metapolicy: Option<MetaPolicy>,
    n_models: u32,
) -> Result<Option<HashSet<Vec<Link>>>, ReasonerError> {
    let n_models_arg = format!("--models={}", n_models).to_string();

    log::info!("solving with {}", n_models_arg);

    let ctl_args = vec![n_models_arg];

    let mut fb = FactBase::new();
    pi.populate(&mut fb)
        .expect("failed at populating the fact base, this is probably an issue with the string identifiers in the links");

    if policies.is_empty() {
        let mut sols = HashSet::new();

        let mut ctl = control(ctl_args.clone()).expect("failed to create control handle");
        ctl.add_facts(&fb).expect("failed to add facts");
        ctl.add("base", &[], PROBLEM_ENCODING)
            .expect("failed to add base problem encoding");

        let parts = vec![Part::new("base", vec![]).expect("failed to create base parts")];
        ctl.ground(&parts).map_err(ReasonerError::AspError)?;

        for model in ctl.all_models().map_err(ReasonerError::AspError)? {
            let path = reconstruct_path(&pi.src, &pi.dst, model.symbols)
                .expect("unable to reconstruct pact from model");
            log::debug!("Path found: {:?}", path);
            sols.insert(path);
        }

        return Ok(Some(sols));
    }

    // TODO: parallelize with rayon
    // solve search problem for every policy
    let mut results = HashMap::new();
    for pol in policies.iter() {
        let mut sols = HashSet::new();

        let mut ctl = control(ctl_args.clone()).expect("failed to create control handle");
        ctl.add_facts(&fb).expect("failed to add facts");
        ctl.add("base", &[], PROBLEM_ENCODING)
            .expect("failed to add base problem encoding");
        ctl.add("base", &[], pol.source())
            .map_err(ReasonerError::AspError)?;

        let parts = vec![Part::new("base", vec![]).expect("failed to create base parts")];
        ctl.ground(&parts).map_err(ReasonerError::AspError)?;

        for model in ctl.all_models().map_err(ReasonerError::AspError)? {
            let path = reconstruct_path(&pi.src, &pi.dst, model.symbols)
                .expect("unable to reconstruct pact from model");
            log::debug!("Path found: {:?}", path);
            sols.insert(path);
        }

        results.insert(pol.id(), sols);
    }

    let mpi = MetaProblemInstance {
        policies: &policies,
        issuers: &issuers,
        metadata: &pi.meta, // TODO: maybe it should be separate
        solutions: &results,
    };

    let mut meta_fb = FactBase::new();
    mpi.populate(&mut meta_fb)
        .map_err(ReasonerError::AspError)?;

    let mut meta_ctl =
        control(vec!["--models=1".to_string()]).expect("failed to create control handle");
    meta_ctl.add_facts(&meta_fb).expect("failed to add facts");
    meta_ctl
        .add("base", &[], META_PROBLEM_ENCODING)
        .map_err(ReasonerError::AspError)?;

    if let Some(mp) = metapolicy {
        meta_ctl
            .add("base", &[], mp.source())
            .map_err(ReasonerError::AspError)?;
        log::debug!("running with meta-policy:\n{}", mp.source());
    }

    let parts = vec![Part::new("base", vec![]).expect("failed to create base parts")];
    meta_ctl.ground(&parts).map_err(ReasonerError::AspError)?;

    let model = meta_ctl
        .all_models()
        .map_err(ReasonerError::AspError)?
        .next()
        .ok_or(ReasonerError::ConflictResolutionError)?;

    for atom in model.symbols.iter() {
        log::debug!("{}", atom.to_string());
        let atom_args = atom.arguments().expect("failed to extract atom args");
        if atom.name().expect("failed to extract atom name") == SYMBOL_DEACTIVATE
            && atom.is_positive().expect("failed to extract atom sign")
        {
            results.remove(
                atom_args
                    .first()
                    .expect("malformed active predicate")
                    .string()
                    .expect("failed to extract symbol string")
                    .parse::<uuid::Uuid>()
                    .expect("malformed policy id")
                    .as_ref(),
            );
        }
    }

    match results.iter().next() {
        None => Ok(None),
        Some((_, sols)) => {
            let mut out = sols.clone();
            for (_, sols) in results.iter() {
                out = out.intersection(sols).cloned().collect();
            }
            Ok(Some(out))
        }
    }
}

#[derive(Debug)]
pub enum ReasonerError {
    AspError(ClingoError),
    ConflictResolutionError,
}

#[derive(Debug, Hash, PartialEq, Eq, Clone)]
pub enum MetadataValue {
    Boolean(bool),
    Numerical(i32),
    Categorical(String),
}

#[derive(Debug, Hash, PartialEq, Eq, Clone)]
pub struct Metadata {
    pub name: String,
    pub value: MetadataValue,
}

#[derive(Debug, Eq, Clone)]
pub struct Link {
    pub as_a: String,
    pub if_a: String,
    pub as_b: String,
    pub if_b: String,
    pub meta: Option<Vec<Metadata>>,
}

impl From<pb::Link> for Link {
    fn from(value: pb::Link) -> Self {
        Link {
            as_a: value.as_a,
            if_a: value.if_a,
            as_b: value.as_b,
            if_b: value.if_b,
            meta: None,
        }
    }
}

impl PartialEq for Link {
    fn eq(&self, other: &Self) -> bool {
        self.as_a == other.as_a
            && self.if_a == other.if_a
            && self.as_b == other.as_b
            && self.if_b == other.if_b
    }
}

impl Hash for Link {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        self.as_a.hash(state);
        self.if_a.hash(state);
        self.as_b.hash(state);
        self.as_b.hash(state);
    }
}

#[derive(Debug)]
pub struct GlobalMetadata {
    pub name: String,
    pub subj: Option<String>,
    pub value: MetadataValue,
}

#[derive(Debug)]
pub struct ProblemInstance {
    pub src: String,
    pub dst: String,
    pub links: Vec<Link>,
    pub meta: Vec<GlobalMetadata>,
}

fn populate_global_metadata(fb: &mut FactBase, data: &GlobalMetadata) -> Result<(), ClingoError> {
    let mut args = match &data.subj {
        Some(subj) => vec![Symbol::create_string(subj)?],
        None => Vec::new(),
    };

    match &data.value {
        MetadataValue::Boolean(v) => fb.insert(&Symbol::create_function(&data.name, &args, *v)?),
        MetadataValue::Numerical(v) => {
            args.push(Symbol::create_number(*v));
            fb.insert(&Symbol::create_function(&data.name, &args, true)?)
        }
        MetadataValue::Categorical(v) => {
            args.push(Symbol::create_string(v)?);
            fb.insert(&Symbol::create_function(&data.name, &args, true)?)
        }
    }

    Ok(())
}

impl ProblemInstance {
    fn populate(&self, fb: &mut FactBase) -> Result<(), ClingoError> {
        fb.insert(&Symbol::create_function(
            SYMBOL_SRC,
            &[Symbol::create_string(&self.src)?],
            true,
        )?);
        fb.insert(&Symbol::create_function(
            SYMBOL_DST,
            &[Symbol::create_string(&self.dst)?],
            true,
        )?);

        for link in self.links.iter() {
            let args = vec![
                Symbol::create_string(&link.as_a)?,
                Symbol::create_string(&link.if_a)?,
                Symbol::create_string(&link.as_b)?,
                Symbol::create_string(&link.if_b)?,
            ];

            fb.insert(&Symbol::create_function(SYMBOL_LINK, &args, true)?);

            if link.meta.is_none() {
                continue;
            }

            for data in link.meta.as_ref().unwrap().iter() {
                match &data.value {
                    MetadataValue::Boolean(v) => {
                        fb.insert(&Symbol::create_function(&data.name, &args, *v)?)
                    }
                    MetadataValue::Numerical(v) => {
                        let mut new_args = args.clone();
                        new_args.push(Symbol::create_number(*v));
                        fb.insert(&Symbol::create_function(&data.name, &new_args, true)?)
                    }
                    MetadataValue::Categorical(v) => {
                        let mut new_args = args.clone();
                        new_args.push(Symbol::create_string(v)?);
                        fb.insert(&Symbol::create_function(&data.name, &new_args, true)?)
                    }
                }
            }
        }

        for data in self.meta.iter() {
            populate_global_metadata(fb, data)?;
        }

        Ok(())
    }
}

fn reconstruct_path(src: &str, dst: &str, symbols: Vec<Symbol>) -> Result<Vec<Link>, ClingoError> {
    let mut out = Vec::with_capacity(symbols.len());
    let mut cur_node: Cow<str> = src.into();
    while cur_node.as_ref() != dst {
        for symbol in symbols
            .iter()
            .filter(|s| s.name().expect("failed to extract symbol name") == SYMBOL_CHOSEN)
        {
            let args = symbol.arguments()?;
            let link = Link {
                as_a: args[0].string()?.to_owned(),
                if_a: args[1].string()?.to_owned(),
                as_b: args[2].string()?.to_owned(),
                if_b: args[3].string()?.to_owned(),
                meta: None,
            };
            if link.as_a == cur_node {
                cur_node = link.as_b.clone().into();
                out.push(link);
            }
        }
    }
    Ok(out)
}

#[derive(Debug)]
pub struct MetaProblemInstance<'a> {
    policies: &'a Vec<Policy>,
    issuers: &'a Vec<Issuer>,
    metadata: &'a Vec<GlobalMetadata>,
    solutions: &'a HashMap<PolicyId, HashSet<Vec<Link>>>,
}

impl MetaProblemInstance<'_> {
    fn populate(&self, fb: &mut FactBase) -> Result<(), ClingoError> {
        for issuer in self.issuers.iter() {
            fb.insert(&Symbol::create_function(
                SYMBOL_POWER,
                &[
                    Symbol::create_string(&issuer.id().to_string())?,
                    Symbol::create_number(issuer.rank()),
                ],
                true,
            )?);
        }

        for pol_a in self.policies.iter() {
            let pol_a_symbol = Symbol::create_string(&pol_a.id().to_string())?;

            match self.issuers.iter().find(|issuer| match pol_a.issuer_id() {
                None => false,
                Some(pol_issuer_id) => pol_issuer_id == issuer.id(),
            }) {
                None => {
                    fb.insert(&Symbol::create_function(
                        SYMBOL_ISSUED,
                        &[
                            Symbol::create_string(&DEFAULT_ISSUER.id().to_string())?,
                            pol_a_symbol,
                            Symbol::create_number(
                                pol_a
                                    .created_at()
                                    .timestamp()
                                    .try_into()
                                    .expect("we do not support i64 timestamps"),
                            ),
                        ],
                        true,
                    )?);
                    log::debug!(
                        "issued({}, {}, {})",
                        &DEFAULT_ISSUER.id().to_string(),
                        pol_a.id().to_string(),
                        pol_a.created_at().timestamp()
                    );
                }
                Some(issuer) => {
                    fb.insert(&Symbol::create_function(
                        SYMBOL_ISSUED,
                        &[
                            Symbol::create_string(&issuer.id().to_string())?,
                            pol_a_symbol,
                            Symbol::create_number(
                                pol_a
                                    .created_at()
                                    .timestamp()
                                    .try_into()
                                    .expect("we do not support i64 timestamps"),
                            ),
                        ],
                        true,
                    )?);
                    log::debug!(
                        "issued({}, {}, {})",
                        issuer.id().to_string(),
                        pol_a.id().to_string(),
                        pol_a.created_at().timestamp()
                    );
                }
            };

            for pol_b in self
                .policies
                .iter()
                .filter(|pol_b| pol_b.id() != pol_a.id())
            {
                let pol_b_symbol = Symbol::create_string(&pol_b.id().to_string())?;

                if self
                    .solutions
                    .get(&pol_a.id())
                    .unwrap()
                    .intersection(self.solutions.get(&pol_b.id()).unwrap())
                    .count()
                    == 0
                {
                    fb.insert(&Symbol::create_function(
                        SYMBOL_CONFLICTING,
                        &[pol_a_symbol, pol_b_symbol],
                        true,
                    )?);
                    log::debug!(
                        "conflicting({}, {})",
                        pol_a.id().to_string(),
                        pol_b.id().to_string()
                    );
                }
            }
        }

        for data in self.metadata.iter() {
            populate_global_metadata(fb, data)?;
        }

        Ok(())
    }
}

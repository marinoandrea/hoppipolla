use std::{
    borrow::Cow,
    collections::{HashMap, HashSet},
    hash::Hash,
    mem,
};

use clingo::{control, ClingoError, FactBase, Part, ShowType, SolveMode, Symbol};

use crate::entities::{Issuer, Policy, PolicyId, DEFAULT_ISSUER};
use crate::policy_manager as pb;

const SYMBOL_SRC: &str = "src";
const SYMBOL_DST: &str = "dst";
const SYMBOL_LINK: &str = "link";
const SYMBOL_CHOSEN: &str = "chosen";
const SYMBOL_ISSUED: &str = "issued";
const SYMBOL_POWER: &str = "power";
const SYMBOL_OVERRIDES: &str = "overrides";
const SYMBOL_CONFLICTING: &str = "conflicting";
const SYMBOL_ACTIVE: &str = "active";

const PROBLEM_ENCODING: &str = "
{ chosen(X, XIF, Y, YIF) : link(X, XIF, Y, YIF) } 1 :- link(X, _, _, _).

% check inclusion of source and destination
:- src(S), not chosen(S, _, _, _).
:- dst(D), not chosen(_, _, D, _).

% check continuity
:- chosen(_, _, Y, _), #count { X : chosen(X, _, Y, _) } != 1, not src(Y).
:- chosen(X, _, _, _), #count { Y : chosen(X, _, Y, _) } != 1, not dst(X).

% check reachability
reachable(S) :- src(S).
reachable(Y) :- reachable(X), chosen(X, _, Y, _).
:- dst(D), not reachable(D).

#show chosen/4.
";

#[derive(Debug)]
pub enum ReasonerError {
    AspError(ClingoError),
    ConflictResolutionError(String),
    InvalidMetaInstance,
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
            args.push(Symbol::create_string(&v)?);
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
            let mut args = vec![
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
                        args.push(Symbol::create_number(*v));
                        fb.insert(&Symbol::create_function(&data.name, &args, true)?)
                    }
                    MetadataValue::Categorical(v) => {
                        args.push(Symbol::create_string(&v)?);
                        fb.insert(&Symbol::create_function(&data.name, &args, true)?)
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

impl<'a> MetaProblemInstance<'a> {
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
                            pol_a_symbol,
                            Symbol::create_string(&DEFAULT_ISSUER.id().to_string())?,
                            Symbol::create_string(&pol_a.created_at().to_rfc3339())?,
                        ],
                        true,
                    )?);
                }
                Some(issuer) => {
                    fb.insert(&Symbol::create_function(
                        SYMBOL_ISSUED,
                        &[
                            pol_a_symbol,
                            Symbol::create_string(&issuer.id().to_string())?,
                            Symbol::create_string(&pol_a.created_at().to_rfc3339())?,
                        ],
                        true,
                    )?);
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
                }
            }
        }

        for data in self.metadata.iter() {
            populate_global_metadata(fb, data)?;
        }

        Ok(())
    }
}

pub fn solve(
    pi: &ProblemInstance,
    policies: Vec<Policy>,
    issuers: Vec<Issuer>,
    metapolicy: Option<&str>,
) -> Result<Option<HashSet<Vec<Link>>>, ReasonerError> {
    let mut fb = FactBase::new();
    pi.populate(&mut fb)
        .expect("failed at populating the fact base, this is probably an issue with the string identifiers in the links");

    // TODO: parallelize with rayon
    // solve search problem for every policy
    let mut results = HashMap::new();
    for pol in policies.iter() {
        let mut sols = HashSet::new();

        let mut ctl = control(vec![]).expect("failed to create control handle");
        ctl.add_facts(&fb).expect("failed to add facts");
        ctl.add("base", &[], PROBLEM_ENCODING)
            .expect("failed to add base problem encoding");
        ctl.add("base", &[], &pol.source())
            .map_err(ReasonerError::AspError)?;

        let parts = vec![Part::new("base", vec![]).expect("failed to create base parts")];
        ctl.ground(&parts).map_err(ReasonerError::AspError)?;

        let mut handle = ctl
            .solve(SolveMode::ASYNC | SolveMode::YIELD, &[])
            .map_err(ReasonerError::AspError)?;

        loop {
            handle.resume().map_err(ReasonerError::AspError)?;
            match handle.model() {
                Ok(Some(model)) => {
                    let atoms = model
                        .symbols(ShowType::SHOWN)
                        .expect("failed to retrieve shown symbols in model");
                    let path = reconstruct_path(&pi.src, &pi.dst, atoms)
                        .expect("unable to reconstruct pact from model");
                    sols.insert(path);
                }
                Ok(None) => break,
                Err(e) => return Err(ReasonerError::AspError(e)),
            }
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

    let mut meta_ctl = control(Vec::new()).expect("failed to create control handle");
    meta_ctl.add_facts(&meta_fb).expect("failed to add facts");

    if let Some(mp_source) = metapolicy {
        meta_ctl
            .add("base", &[], mp_source)
            .map_err(ReasonerError::AspError)?;
    }

    let parts = vec![Part::new("base", vec![]).expect("failed to create base parts")];
    meta_ctl.ground(&parts).map_err(ReasonerError::AspError)?;

    let mut handle = meta_ctl
        .solve(SolveMode::ASYNC | SolveMode::YIELD, &[])
        .map_err(ReasonerError::AspError)?;

    handle.resume().map_err(ReasonerError::AspError)?;

    let mut overridden_policies: HashSet<Symbol> = HashSet::with_capacity(policies.len());
    let mut deactivated_policies: HashSet<Symbol> = HashSet::with_capacity(policies.len());
    let mut unresolved_conflicts: Vec<&Symbol> =
        Vec::with_capacity((policies.len() * policies.len()) / 2);

    match handle.model() {
        Err(e) => return Err(ReasonerError::AspError(e)),
        Ok(None) => return Err(ReasonerError::InvalidMetaInstance),
        Ok(Some(model)) => {
            let atoms = model
                .symbols(ShowType::ALL)
                .expect("failed to retrieve shown symbols in meta-model");

            for activation in atoms
                .iter()
                .filter(|s| s.name().expect("failed to extract symbol name") == SYMBOL_ACTIVE)
            {
                deactivated_policies.insert(
                    activation
                        .arguments()
                        .expect("failed to extract active argument")
                        .get(0)
                        .expect("malformed active predicate")
                        .to_owned(),
                );
            }

            let mut conflicts: Vec<&Symbol> = atoms
                .iter()
                .filter(|s| s.name().expect("failed to extract symbol name") == SYMBOL_CONFLICTING)
                .collect();

            loop {
                for conflict in conflicts.iter() {
                    let conflicting_policies = conflict
                        .arguments()
                        .expect("failed to extract conflicting arguments");
                    let pol_a = conflicting_policies
                        .get(0)
                        .expect("faulty definition of conflicting a")
                        .to_owned();
                    let pol_b = conflicting_policies
                        .get(1)
                        .expect("faulty definition of conflicting b")
                        .to_owned();

                    if overridden_policies.contains(&pol_a)
                        || overridden_policies.contains(&pol_b)
                        || deactivated_policies.contains(&pol_a)
                        || deactivated_policies.contains(&pol_b)
                    {
                        continue;
                    }

                    let a_overrides_b =
                        Symbol::create_function(SYMBOL_OVERRIDES, &[pol_a, pol_b], true)
                            .map_err(ReasonerError::AspError)?;
                    let b_overrides_a =
                        Symbol::create_function(SYMBOL_OVERRIDES, &[pol_b, pol_a], true)
                            .map_err(ReasonerError::AspError)?;

                    if model
                        .contains(a_overrides_b)
                        .map_err(ReasonerError::AspError)?
                    {
                        overridden_policies.insert(pol_b);
                    } else if model
                        .contains(b_overrides_a)
                        .map_err(ReasonerError::AspError)?
                    {
                        overridden_policies.insert(pol_a);
                    } else {
                        unresolved_conflicts.push(conflict);
                    }
                }

                if conflicts.len() == unresolved_conflicts.len() {
                    break;
                }

                mem::swap(&mut conflicts, &mut unresolved_conflicts);
                unresolved_conflicts.clear();
            }

            if let Some(conflict) = unresolved_conflicts.pop() {
                return Err(ReasonerError::ConflictResolutionError(conflict.to_string()));
            }
        }
    }

    let mut valid_results = results.iter().filter(|(pol, _)| {
        let pol_symbol = &Symbol::create_string(&pol.to_string())
            .map_err(ReasonerError::AspError)
            .unwrap();
        return !overridden_policies.contains(pol_symbol)
            && !deactivated_policies.contains(pol_symbol);
    });

    match valid_results.next() {
        None => return Ok(None),
        Some((_, sols)) => {
            let mut out = sols.clone();
            for (_, sols) in valid_results {
                out = out.intersection(sols).cloned().collect();
            }
            return Ok(Some(out));
        }
    }
}

/*
fn main() -> Result<(), std::io::Error> {
    let pi = ProblemInstance {
        src: "1".to_string(),
        dst: "4".to_string(),
        meta: vec![
            GlobalMetadata {
                name: "under_ddos".to_string(),
                subj: None,
                value: MetadataValue::Boolean(true),
            },
            GlobalMetadata {
                name: "located".to_string(),
                subj: Some("1".to_string()),
                value: MetadataValue::Categorical("Italy".to_string()),
            },
        ],
        links: Vec::from([
            Link {
                meta: Some(vec![
                    Metadata {
                        name: "test".to_string(),
                        value: MetadataValue::Boolean(false),
                    },
                    Metadata {
                        name: "meaningoflife".to_string(),
                        value: MetadataValue::Numerical(42),
                    },
                    Metadata {
                        name: "status".to_string(),
                        value: MetadataValue::Categorical("busy".to_string()),
                    },
                ]),
                as_a: "1".to_string(),
                if_a: "1".to_string(),
                as_b: "2".to_string(),
                if_b: "1".to_string(),
            },
            Link {
                meta: None,
                as_a: "1".to_string(),
                if_a: "3".to_string(),
                as_b: "2".to_string(),
                if_b: "3".to_string(),
            },
            Link {
                meta: None,
                as_a: "1".to_string(),
                if_a: "2".to_string(),
                as_b: "3".to_string(),
                if_b: "1".to_string(),
            },
            Link {
                meta: None,
                as_a: "2".to_string(),
                if_a: "2".to_string(),
                as_b: "4".to_string(),
                if_b: "1".to_string(),
            },
            Link {
                meta: None,
                as_a: "3".to_string(),
                if_a: "2".to_string(),
                as_b: "4".to_string(),
                if_b: "2".to_string(),
            },
        ]),
    };

    let policies = vec![
        Policy {
            id: "1".to_string(),
            src: ":- chosen(X, _, _, _), located(X, \"Italy\").".to_string(),
            issued_at: Utc::now(),
            meta: None,
        },
        Policy {
            id: "2".to_string(),
            src: ":- chosen(X, _, _, _), located(X, \"France\").".to_string(),
            issued_at: Utc::now(),
            meta: None,
        },
        Policy {
            id: "3".to_string(),
            src: ":- chosen(X, _, _, _), located(X, \"Papua New Guinea\").".to_string(),
            issued_at: Utc::now(),
            meta: None,
        },
    ];

    let res = solve(
        &pi,
        policies,
        "
    superior_overrides(P1, P2)  :- conflicting(P1, P2),
        issuer(S1, P1), issuer(S2, P2),
        power(S1, R1), power(S2, R2),
        R1 < R2.

    posterior_overrides(P1, P2) :- conflicting(P1, P2),
        issuer(S1, P1), issuer(S2, P2),
        power(S1, R1), power(S2, R2),
        issued(P1, T1), issued(P2, T2),
        R1 = R2,
        T1 > T2.

    overrides(A, B) :- superior_overrides(A, B).
    overrides(A, B) :- posterior_overrides(A, B).
    ",
    )
    .unwrap();

    println!("{:?}", res);

    Ok(())
}

    Example of metadata for MetaProblemInstance

    pol_a: [
        {
            "name": "issuer",
            "value": "gov-a",
        }
    ],
    pol_b: [
        {
            "name": "issuer",
            "value": "eu-a",
        }
    ],
    pol_c: [
        {
            "name": "issuer",
            "value": "gov-b",
        }
    ],
    global: [
        {
            "name": "power"
            "target": "gov-a",
            "value": 3
        },
        {
            "name": "power"
            "target": "eu-a",
            "value": 5
        },
        {
            "name": "power"
            "target": "gov-b",
            "value": 3
        },
    ]
    }
*/

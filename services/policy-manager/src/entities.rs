use crate::policy_manager as pb;
use std::{error::Error, time::SystemTime};

use chrono::{DateTime, Utc};
use lazy_static::lazy_static;
use uuid::Uuid;

pub type PolicyId = Uuid;
pub type IssuerId = Uuid;
pub type MetaPolicyId = Uuid;

#[derive(Clone, Debug, sqlx::FromRow, sqlxinsert::PgInsert)]
pub struct Policy {
    id: PolicyId,
    created_at: DateTime<Utc>,
    updated_at: DateTime<Utc>,
    issuer_id: Option<IssuerId>,
    title: Option<String>,
    description: Option<String>,
    source: String,
}

impl Policy {
    pub fn new(
        issuer_id: Option<IssuerId>,
        title: Option<String>,
        description: Option<String>,
        source: String,
    ) -> Result<Self, Box<dyn Error>> {
        check_syntax(&source)?;
        Ok(Self {
            id: Uuid::new_v4(),
            created_at: Utc::now(),
            updated_at: Utc::now(),
            issuer_id,
            title,
            description,
            source,
        })
    }

    pub fn id(&self) -> PolicyId {
        self.id
    }

    pub fn created_at(&self) -> &DateTime<Utc> {
        &self.created_at
    }

    pub fn updated_at(&self) -> &DateTime<Utc> {
        &self.updated_at
    }

    pub fn issuer_id(&self) -> Option<IssuerId> {
        self.issuer_id
    }

    pub fn title(&self) -> &Option<String> {
        &self.title
    }

    pub fn description(&self) -> &Option<String> {
        &self.description
    }

    pub fn source(&self) -> &String {
        &self.source
    }

    pub fn set_title(&mut self, title: Option<String>) {
        self.title = title;
        self.updated_at = Utc::now();
    }

    pub fn set_description(&mut self, description: Option<String>) {
        self.description = description;
        self.updated_at = Utc::now();
    }

    pub fn set_source(&mut self, source: String) -> Result<(), Box<dyn Error>> {
        check_syntax(&source)?;
        self.source = source;
        self.updated_at = Utc::now();
        Ok(())
    }
}

impl From<&Policy> for pb::Policy {
    fn from(value: &Policy) -> Self {
        Self {
            id: value.id.to_string(),
            created_at: Some(SystemTime::from(value.created_at).into()),
            updated_at: Some(SystemTime::from(value.updated_at).into()),
            issuer_id: value.issuer_id.map(|id| id.to_string()),
            title: value.title.clone(),
            description: value.description.clone(),
            source: value.source.clone(), // TODO: change name?
        }
    }
}

fn check_syntax(source: &str) -> Result<(), Box<dyn Error>> {
    let mut ctl = clingo::control(vec![]).expect("failed to create clingo::Control");
    ctl.add("base", &[], source)?;
    Ok(())
}

#[derive(Clone, Debug, sqlx::FromRow, sqlxinsert::PgInsert)]
pub struct Issuer {
    id: IssuerId,
    created_at: DateTime<Utc>,
    updated_at: DateTime<Utc>,
    name: String,
    rank: i32,
    description: Option<String>,
}

impl Issuer {
    pub fn new(name: String, rank: i32, description: Option<String>) -> Self {
        Self {
            id: Uuid::new_v4(),
            created_at: Utc::now(),
            updated_at: Utc::now(),
            name,
            rank,
            description,
        }
    }

    pub fn id(&self) -> PolicyId {
        self.id
    }

    pub fn created_at(&self) -> &DateTime<Utc> {
        &self.created_at
    }

    pub fn updated_at(&self) -> &DateTime<Utc> {
        &self.updated_at
    }

    pub fn rank(&self) -> i32 {
        self.rank
    }
}

impl From<&Issuer> for pb::Issuer {
    fn from(value: &Issuer) -> Self {
        Self {
            id: value.id.to_string(),
            created_at: Some(SystemTime::from(value.created_at).into()),
            updated_at: Some(SystemTime::from(value.updated_at).into()),
            name: value.name.clone(),
            description: value.description.clone(),
        }
    }
}

lazy_static! {
    pub static ref DEFAULT_ISSUER: Issuer = Issuer {
        id: Uuid::new_v4(),
        created_at: Utc::now(),
        updated_at: Utc::now(),
        name: "default".to_string(),
        description: None,
        rank: 0,
    };
}

#[derive(Clone, Debug, sqlx::FromRow, sqlxinsert::PgInsert)]
pub struct MetaPolicy {
    id: MetaPolicyId,
    created_at: DateTime<Utc>,
    updated_at: DateTime<Utc>,
    title: Option<String>,
    description: Option<String>,
    source: String,
}

impl MetaPolicy {
    pub fn new(
        title: Option<String>,
        description: Option<String>,
        source: String,
    ) -> Result<Self, Box<dyn Error>> {
        check_syntax(&source)?;
        Ok(Self {
            id: Uuid::new_v4(),
            created_at: Utc::now(),
            updated_at: Utc::now(),
            title,
            description,
            source,
        })
    }

    pub fn id(&self) -> MetaPolicyId {
        self.id
    }

    pub fn created_at(&self) -> &DateTime<Utc> {
        &self.created_at
    }

    pub fn updated_at(&self) -> &DateTime<Utc> {
        &self.updated_at
    }

    pub fn title(&self) -> &Option<String> {
        &self.title
    }

    pub fn description(&self) -> &Option<String> {
        &self.description
    }

    pub fn source(&self) -> &String {
        &self.source
    }

    pub fn set_title(&mut self, title: Option<String>) {
        self.title = title;
        self.updated_at = Utc::now();
    }

    pub fn set_description(&mut self, description: Option<String>) {
        self.description = description;
        self.updated_at = Utc::now();
    }

    pub fn set_source(&mut self, source: String) -> Result<(), Box<dyn Error>> {
        check_syntax(&source)?;
        self.source = source;
        self.updated_at = Utc::now();
        Ok(())
    }
}

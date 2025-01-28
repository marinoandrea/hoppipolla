use core::panic;

use sqlx::{migrate::MigrateDatabase, postgres::*, Pool};

use crate::entities::{Issuer, MetaPolicy, Policy, PolicyId};

// NOTE: we introduce an arbitrary upper limit that should never be exceeded in
// a real world scenario. Policies are stored in memory during execution
// therefore they are not supposed to grow infinetely.
static MAX_POLICIES: i32 = 10_000;

pub struct PolicyDb {
    pool: Pool<Postgres>,
}

// NOTE: failed operations on core domain operations cause a panic acting as
// runtime asserts. We should not be running with a broken database connection.
impl PolicyDb {
    pub async fn load_policies(&self) -> Vec<Policy> {
        sqlx::query_as("SELECT * FROM policies LIMIT $1;")
            .bind(MAX_POLICIES)
            .fetch_all(&self.pool)
            .await
            .inspect_err(|e| log::error!("{}", e))
            .expect("could not load policies from database")
    }

    pub async fn load_issuers(&self) -> Vec<Issuer> {
        sqlx::query_as("SELECT * FROM issuers LIMIT $1;")
            .bind(MAX_POLICIES)
            .fetch_all(&self.pool)
            .await
            .inspect_err(|e| log::error!("{}", e))
            .expect("could not load issuers from database")
    }

    pub async fn load_meta_policy(&self) -> Option<MetaPolicy> {
        match sqlx::query_as("SELECT * FROM meta_policies ORDER BY created_at DESC LIMIT 1;")
            .fetch_one(&self.pool)
            .await
        {
            Err(err) => match err {
                sqlx::Error::RowNotFound => None,
                _ => panic!("could not load meta policy from database"),
            },
            Ok(row) => Some(row),
        }
    }

    pub async fn tx(&self) -> sqlx::Transaction<Postgres> {
        self.pool
            .begin()
            .await
            .inspect_err(|e| log::error!("{}", e))
            .expect("could not begin a transaction")
    }

    pub async fn insert_policy<'e, E>(&self, executor: E, p: &Policy) -> Result<(), sqlx::Error>
    where
        E: sqlx::Executor<'e, Database = sqlx::Postgres>,
    {
        p.insert_ex(executor, "policies").await
    }

    pub async fn delete_policy<'e, E>(
        &self,
        executor: E,
        id: &PolicyId,
    ) -> Result<sqlx::postgres::PgQueryResult, sqlx::Error>
    where
        E: sqlx::Executor<'e, Database = sqlx::Postgres>,
    {
        sqlx::query("DELETE FROM policies WHERE id = $1 RETURNING *;")
            .bind(id)
            .execute(executor)
            .await
    }

    pub async fn update_policy<'e, E>(&self, executor: E, p: &Policy) -> Result<(), sqlx::Error>
    where
        E: sqlx::Executor<'e, Database = sqlx::Postgres>,
    {
        p.update_ex(executor, "policies").await
    }

    pub async fn insert_issuer<'e, E>(&self, executor: E, i: &Issuer) -> Result<(), sqlx::Error>
    where
        E: sqlx::Executor<'e, Database = sqlx::Postgres>,
    {
        i.insert_ex(executor, "issuers").await
    }

    pub async fn update_issuer<'e, E>(&self, executor: E, i: &Issuer) -> Result<(), sqlx::Error>
    where
        E: sqlx::Executor<'e, Database = sqlx::Postgres>,
    {
        i.update_ex(executor, "issuers").await
    }

    pub async fn new(url: &str, max_connections: u32) -> PolicyDb {
        if !Postgres::database_exists(url)
            .await
            .inspect_err(|e| log::error!("{}", e))
            .expect("could not check if database exists")
        {
            Postgres::create_database(url)
                .await
                .inspect_err(|e| log::error!("{}", e))
                .expect("could not create database");
        }

        let pool = PgPoolOptions::new()
            .max_connections(max_connections)
            .connect(url)
            .await
            .inspect_err(|e| log::error!("{}", e))
            .expect("could not connect to database");

        // we are building a framework, not an application, no need for migrations
        sqlx::query(
            "
            CREATE TABLE IF NOT EXISTS policies (
                id          UUID PRIMARY KEY,
                created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                issuer_id   UUID NOT NULL,
                title       TEXT,
                description TEXT,
                source      TEXT NOT NULL,

                FOREIGN KEY (issuer_id) REFERENCES issuers(id)
            );
            
            CREATE TABLE IF NOT EXISTS issuers (
                id          UUID PRIMARY KEY,
                created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                name        TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS meta_policies (
                id          UUID PRIMARY KEY,
                created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                updated_at  TIMESTAMP WITH TIME ZONE NOT NULL,
                title       TEXT,
                description TEXT,
                source      TEXT NOT NULL,
            );
        ",
        )
        .execute(&pool)
        .await
        .inspect_err(|e| log::error!("{}", e))
        .expect("could not initialize database");

        PolicyDb { pool }
    }
}

"""initial chronos schema
Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0001_initial"; down_revision=None; branch_labels=None; depends_on=None
def _base(table, columns):
    op.create_table(table,sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),*columns,sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.text("now()")),sa.Column("updated_at",sa.DateTime(timezone=True),server_default=sa.text("now()")))
def upgrade():
    _base("users",[sa.Column("email",sa.String(320),unique=True,nullable=False),sa.Column("name",sa.String(120),nullable=False),sa.Column("avatar_url",sa.String(2048)),sa.Column("github_id",sa.String(64),unique=True),sa.Column("is_active",sa.Boolean,server_default=sa.true(),nullable=False)])
    _base("repositories",[sa.Column("owner_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("provider",sa.String(30),nullable=False),sa.Column("external_id",sa.String(100),nullable=False),sa.Column("full_name",sa.String(300),unique=True,nullable=False),sa.Column("default_branch",sa.String(255),nullable=False),sa.Column("is_active",sa.Boolean,server_default=sa.true(),nullable=False)])
    _base("pull_requests",[sa.Column("repository_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("repositories.id"),nullable=False),sa.Column("number",sa.Integer,nullable=False),sa.Column("title",sa.String(500),nullable=False),sa.Column("author",sa.String(120),nullable=False),sa.Column("head_sha",sa.String(64),nullable=False),sa.Column("base_branch",sa.String(255),nullable=False),sa.Column("status",sa.String(40),nullable=False),sa.Column("diff",sa.Text),sa.UniqueConstraint("repository_id","number",name="uq_pr_repo_number")])
    _base("analysis_history",[sa.Column("pull_request_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("pull_requests.id"),nullable=False),sa.Column("status",sa.Enum("queued","running","completed","failed",name="analysisstatus"),nullable=False),sa.Column("pre_mortem",sa.Text),sa.Column("completed_at",sa.DateTime(timezone=True))])
    _base("agent_results",[sa.Column("analysis_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("analysis_history.id"),nullable=False),sa.Column("agent_name",sa.String(100),nullable=False),sa.Column("status",sa.String(30),nullable=False),sa.Column("result",sa.JSON,nullable=False),sa.Column("confidence",sa.Float)])
    _base("risk_scores",[sa.Column("analysis_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("analysis_history.id"),unique=True,nullable=False),sa.Column("score",sa.Integer,nullable=False),sa.Column("level",sa.String(20),nullable=False),sa.Column("factors",sa.JSON,nullable=False)])
    _base("simulation_results",[sa.Column("analysis_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("analysis_history.id"),nullable=False),sa.Column("scenario",sa.String(255),nullable=False),sa.Column("outcome",sa.JSON,nullable=False)])
    _base("feedback",[sa.Column("analysis_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("analysis_history.id"),nullable=False),sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("rating",sa.Integer,nullable=False),sa.Column("comment",sa.Text)])
    _base("incident_reports",[sa.Column("analysis_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("analysis_history.id"),unique=True,nullable=False),sa.Column("title",sa.String(500),nullable=False),sa.Column("report",sa.Text,nullable=False),sa.Column("rollback_plan",sa.Text),sa.Column("counter_pr",sa.JSON,nullable=False)])
    _base("settings",[sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("key",sa.String(100),nullable=False),sa.Column("value",sa.JSON,nullable=False),sa.UniqueConstraint("user_id","key",name="uq_setting_user_key")])
def downgrade():
    for table in ["settings","incident_reports","feedback","simulation_results","risk_scores","agent_results","analysis_history","pull_requests","repositories","users"]: op.drop_table(table)
    op.execute("DROP TYPE IF EXISTS analysisstatus")

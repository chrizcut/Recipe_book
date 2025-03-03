"""added everything at once

Revision ID: 1407ab9ddad2
Revises: 
Create Date: 2025-03-01 11:22:48.932266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1407ab9ddad2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_recipe_user'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipe_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_recipe_user_id'), ['user_id'], unique=False)

    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], name='fk_ingredient_recipe'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ingredient', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ingredient_recipe_id'), ['recipe_id'], unique=False)

    op.create_table('step',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('step', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_step_recipe_id'), ['recipe_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('step', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_step_recipe_id'))

    op.drop_table('step')
    with op.batch_alter_table('ingredient', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ingredient_recipe_id'))

    op.drop_table('ingredient')
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipe_user_id'))
        batch_op.drop_index(batch_op.f('ix_recipe_name'))

    op.drop_table('recipe')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))

    op.drop_table('user')
    # ### end Alembic commands ###

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.sql import operators

class ilike(operators.ColumnOperators):
    """Custom operator for ILIKE functionality in SQLAlchemy."""
    def operate(self, op, other):
        return BinaryExpression(self, other, operators.custom_op("ILIKE"))

@compiles(ilike, 'postgresql')
def _compile_ilike(element, compiler, **kw):
    """Compile the ILIKE operator for PostgreSQL."""
    left = compiler.process(element.left, **kw)
    right = compiler.process(element.right, **kw)
    return f"{left} ILIKE {right}"

# Example usage:
# query = session.query(User).filter(User.name.ilike('%john%'))
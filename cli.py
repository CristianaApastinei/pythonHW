import click
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel, Field, ValidationError


class OperationInput(BaseModel):
    operation: str = Field(..., description="Operation: pow, fib, fact")
    x: int = Field(..., ge=0)
    y: int = Field(default=0, ge=0)


def compute_pow(x, y):
    return x ** y


def compute_fact(n):
    if n == 0:
        return 1
    return n * compute_fact(n - 1)


def compute_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


async def execute_operation(op_data: OperationInput):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        if op_data.operation == "pow":
            result = await loop.run_in_executor(pool, compute_pow, op_data.x, op_data.y)
        elif op_data.operation == "fib":
            result = await loop.run_in_executor(pool, compute_fib, op_data.x)
        elif op_data.operation == "fact":
            result = await loop.run_in_executor(pool, compute_fact, op_data.x)
        else:
            raise ValueError("Unsupported operation")
    return result


@click.command()
@click.option('--operation', required=True, type=click.Choice(['pow', 'fib', 'fact']), help='Math operation')
@click.option('--x', required=True, type=int, help='First operand')
@click.option('--y', default=0, type=int, help='Second operand (used only for pow)')
def main(operation, x, y):
    try:
        data = OperationInput(operation=operation, x=x, y=y)
    except ValidationError as e:
        click.echo(e.json())
        return

    result = asyncio.run(execute_operation(data))
    click.echo(f"Result of {operation} is: {result}")


if __name__ == "__main__":
    main()

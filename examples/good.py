"""Small, tidy example module used by fuck-your-code's own tests.

It calculates simple statistics for a list of numbers and formats
the result for display. Nothing clever, just clean.
"""

from dataclasses import dataclass


@dataclass
class Summary:
    """Container for the computed statistics."""

    count: int
    total: float
    average: float
    maximum: float


def compute_summary(values):
    """Return a Summary for a non-empty list of numbers.

    Raises ValueError when the input is empty, because an average
    of nothing is a lie we refuse to tell.
    """
    if not values:
        raise ValueError("values must not be empty")
    total = sum(values)
    return Summary(
        count=len(values),
        total=total,
        average=total / len(values),
        maximum=max(values),
    )


def format_summary(summary):
    """Render a Summary as a short human-readable string."""
    return (
        f"count={summary.count} total={summary.total:.2f} "
        f"average={summary.average:.2f} max={summary.maximum:.2f}"
    )


def load_numbers(path):
    """Read one number per line from a text file.

    Blank lines are skipped. A malformed line raises ValueError
    with the offending line number so the caller can fix the file.
    """
    numbers = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            text = raw_line.strip()
            if not text:
                continue
            try:
                numbers.append(float(text))
            except ValueError:
                raise ValueError(
                    f"line {line_number} is not a number: {text!r}"
                ) from None
    return numbers


def main():
    """Demo entry point: summarize a fixed sample of readings."""
    sample_readings = [12.5, 9.0, 14.25, 11.0, 10.75]
    summary = compute_summary(sample_readings)
    print(format_summary(summary))


if __name__ == "__main__":
    main()

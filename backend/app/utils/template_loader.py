from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

# Path to your templates folder
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

# Initialize Jinja environment
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)

# ---------- CUSTOM FILTERS ----------

def euro(value):
    """
    Format a numeric value as Euro currency.
    Example: 10250.75 → "10 250,75 €"
    """
    try:
        return f"{float(value):,.2f} €".replace(",", "X").replace(".", ",").replace("X", " ")
    except Exception:
        return f"{value} €"

def usd(value):
    """
    Format a numeric value as USD currency.
    Example: 10500.5 → "$10,500.50"
    """
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return f"${value}"

def xof(value):
    """
    Format a numeric value as XOF (CFA franc).
    Example: 250000 → "250 000 F CFA"
    """
    try:
        return f"{int(value):,}".replace(",", " ") + " F CFA"
    except Exception:
        return f"{value} F CFA"

# Register filters
env.filters["euro"] = euro
env.filters["usd"] = usd
env.filters["xof"] = xof


# ---------- TEMPLATE RENDERER ----------

def render_html_template(template_name: str, **kwargs) -> str:
    """
    Renders a Jinja2 HTML template with provided variables.
    Example: render_html_template("weekly_email.html", user=user, portfolio_value=10500)
    """
    template = env.get_template(template_name)
    return template.render(**kwargs)

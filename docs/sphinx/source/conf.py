"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
import os
import sys
import toml

py_project = toml.load(os.path.abspath("../../../pyproject.toml"))

# pylint: disable=invalid-name
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = os.getenv('APP_NAME', 'FastAPI Application')
author = py_project['tool']['poetry']['authors'][0]
release = py_project['tool']['poetry']['version']
# pylint: disable=redefined-builtin
copyright = '2025, <Your Name/Organisation Here>'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../../../'))

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}
source_encoding = 'utf-8'
root_doc = 'modules'

extensions = [
    # Built-in extensions
    'sphinx.ext.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinx.ext.coverage",
    'sphinx.ext.duration',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',

    # Third party extensions
    'sphinx_autodoc_typehints',
    'sphinx_favicon',
    'sphinxcontrib.httpdomain'
]

# --- Extension configurations -----------------------------------------------
# Disable module name prefixes in documentation
add_module_names = False

# --- Settings for extention 'sphinx.ext.apidoc' -----------------------------
apidoc_modules = [
    {
        'path': '../../../src/',  # Path to your Python package
        'destination': './',  # Output directory for generated files
        'max_depth': 2,  # Maximum depth of submodules
        'follow_links': False,  # Do not follow symbolic links
        'separate_modules': True,  # Combine modules into a single page
        'include_private': True,  # Exclude private modules
        'no_headings': False,  # Generate headings for modules
        'module_first': False,  # Place module documentation before submodules
        'implicit_namespaces': True,  # Use PEP 420 implicit namespaces
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'special-members',
        },
        'exclude_patterns': [
            '**/logs/*',
            '**/tests/*',
            '**/migrations/*'
        ],
    },
]

# --- Settings for extention 'sphinx.ext.autosummary' ------------------------
autosummary_generate = True
autosummary_generate_overwrite = True  # Overwrite existing stub files
autosummary_imported_members = False  # Exclude imported members
autosummary_ignore_module_all = True  # Ignore __all__ attribute in modules
autosummary_filename_map = {}  # Map object names to filenames

# Autodoc Extension settings
autodoc_typehints = 'description'
# --- Autodoc Extension settings ---------------------------------------------
autodoc_mock_imports = [
    # Alembic and related libraries
    'alembic',

    # SQLAlchemy and related libraries
    'sqlalchemy',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.orm',

    # FastAPI, PostgreSQL, and related libraries
    'src.db.migrations.psql',
    'src.db.migrations.psql.env',
    'src.db.migrations.mongodb'
]

# --- Settings for extention 'sphinx.ext.napoleon' ---------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# --- Settings for extention 'sphinx.ext.intersphinx' ------------------------
# intersphinx_resolve_self = ''
# intersphinx_cache_limit = 5
# intersphinx_timeout = None
# intersphinx_disabled_reftypes = ['str:doc']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/13', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
}


# --- Settings for extension 'sphinx.ext.linkcode' ---------------------------
def linkcode_resolve(domain, info):
    """
    Resolve the URL for the source code of a given object.
    """
    if domain != 'py':  # Only handle Python objects
        return None
    if not info.get('module'):  # Ensure the module is specified
        return None

    # Replace dots with slashes to form the file path
    filename = info['module'].replace('.', '/')
    # Add the object name if available
    # object_name = info.get('fullname', '')

    # Construct the GitHub URL (adjust branch and repo as needed)
    # pylint: disable=line-too-long
    return f"https://github.com/DanneDevOoops/fastApi-v1/blob/main/{filename}.py#L1"


# pylint: disable=self-assigning-variable
linkcode_resolve = linkcode_resolve

# Settings for extension 'sphinx.ext.to-do' (- separated to avoid marker) ----
todo_include_todos = True
todo_emit_warnings = False
todo_link_only = False

# --- Settings for 'sphinx.ext.coverage' -------------------------------------
coverage_modules = ['src']

# Ignore specific modules, functions, classes, or objects using regex
coverage_ignore_modules = [
    'src.db.migrations',
    'src.db.migrations.psql',
    'src.db.migrations.mongodb',
]
coverage_ignore_functions = [r'^test_.*']
coverage_ignore_classes = []
coverage_ignore_pyobjects = []

# Additional options
coverage_write_headline = True  # Write headlines in the report
coverage_skip_undoc_in_source = False  # Include objects without docstrings
coverage_show_missing_items = False  # Print missing items to stdout
coverage_statistics_to_report = True  # Include a tabular report in the output
coverage_statistics_to_stdout = True  # Print the tabular report to stdout

# --- Settings for 'sphinx.ext.graphviz' -------------------------------------
graphviz_dot = 'dot'
graphviz_dot_args = ['-Gdpi=300']
graphviz_output_format = 'svg'

# --- Settings for 'sphinx-favicon' ------------------------------------------
# favicons = [
#     {
#         "sizes": "16x16",
#         "href": "https://secure.example.com/favicon/favicon-16x16.png",
#     },
#     {
#         "sizes": "32x32",
#         "href": "https://secure.example.com/favicon/favicon-32x32.png",
#     },
#     {
#         "rel": "apple-touch-icon",
#         "sizes": "180x180",
#         "href": "some.png",  # use a local file in _static
#     },
# ]

# --- Settings for 'sphinx-autodoc-typehints' --------------------------------
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True
typehints_use_rtype = True
typehints_defaults = 'comma'
simplify_optional_unions = True
typehints_use_signature = False
typehints_use_signature_return = False

# -- Options for HTMLHelp output ---------------------------------------------
templates_path = ['_templates']
exclude_patterns = [
    '.github/',
    'db_dumps/',
    'docs/',
    'logs/',
    '**/db_scripts/*'
    'src/db/migrations',
    'tests/',
    '_build/',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Documentation root path
# html_baseurl = 'https://dmoest.github.io/ekobot_fast_api/'

# -- Options for HTMLHelp output ---------------------------------------------
html_theme_options = {
    'navigation_depth': 10,
    'prev_next_buttons_location': 'bottom',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': True,
    'style_external_links': True,
    'style_nav_header_background': '#0095b9',
}

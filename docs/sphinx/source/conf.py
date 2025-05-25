"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from datetime import datetime
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
copyright = '2025, %s', author

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../../../'))
root_doc = 'index'
source_encoding = 'utf-8-sig'
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

extensions = [
    # Built-in extensions
    'sphinx.ext.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    "sphinx.ext.coverage",
    'sphinx.ext.duration',
    'sphinx.ext.graphviz',
    'sphinx.ext.imgconverter',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',

    # Third party extensions
    'sphinx_autodoc_typehints',
    'sphinx_favicon',
    'myst_parser'
]

# --- Built-in configurations ------------------------------------------------
toc_object_entries = True
toc_object_entries_show_parents = 'all'

# --- Extension configurations -----------------------------------------------
# Disable module name prefixes in documentation
add_module_names = False

# --- Settings for extention 'sphinx.ext.apidoc' -----------------------------
apidoc_modules = [
    {
        'path': '../../../src/api',
        'destination': './rst/api',
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': True,
        'include_private': True,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': True,
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'imported-members'
        },
        'exclude_patterns': [
            '**/migrations/*',
            '**/migrations/psql/**/*',
            '**/migrations/mongodb/**/*',
        ],
    },
    {
        'path': '../../../src/core',
        'destination': './rst/core',
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': True,
        'include_private': True,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': True,
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'special-members'
        },
        'exclude_patterns': [
            '**/migrations/*',
            '**/migrations/psql/**/*',
            '**/migrations/mongodb/**/*',
        ],
    },
    {
        'path': '../../../src/db',
        'destination': './rst/db',
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': True,
        'include_private': True,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': True,
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'special-members'
        },
        'exclude_patterns': [
            '**/config/base.py',
            '**/migrations/*',
            '**/migrations/psql',
            '**/migrations/psql/env',
            '**/migrations/psql/versions',
            '**/migrations/mongodb/**/*',
        ],
    },
    {
        'path': '../../../src/middlewares',
        'destination': './rst/middlewares',
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': True,
        'include_private': True,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': True,
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'special-members'
        },
        'exclude_patterns': [
            '**/migrations/*',
            '**/migrations/psql/**/*',
            '**/migrations/mongodb/**/*',
        ],
    },
    {
        'path': '../../../src/utils',
        'destination': './rst/utils',
        'max_depth': 4,
        'follow_links': False,
        'separate_modules': True,
        'include_private': True,
        'no_headings': False,
        'module_first': False,
        'implicit_namespaces': True,
        'automodule_options': {
            'members',
            'show-inheritance',
            'undoc-members',
            'private-members',
            'special-members'
        },
        'exclude_patterns': [
            '**/migrations/*',
            '**/migrations/psql/**/*',
            '**/migrations/mongodb/**/*',
        ],
    },
]

# --- Settings for extention 'sphinx.ext.autosummary' ------------------------
autosummary_generate = True
autosummary_generate_overwrite = False
autosummary_imported_members = False
autosummary_ignore_module_all = True
autosummary_filename_map = {}

# Autodoc Extension settings
autodoc_typehints = 'description'

# --- Settings fo 'sphinx.ext.autosectionlabel' ------------------------------
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = None

# --- Settings for 'sphinx.ext.autodoc' --------------------------------------
autodoc_mock_imports = [
    # Alembic related libraries
    'alembic',

    # FastAPI related libraries
    'fastapi',

    # SQLAlchemy related libraries
    'sqlalchemy',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.orm',

    # Database related libraries
    'src.db.migrations.psql',
    'src.db.migrations.psql.env',
    'src.db.migrations.psql.versions',
    'src.db.migrations.mongodb',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'inherited-members': False,
    'show-inheritance': True,
}

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

# --- Settings for 'sphinx.ext.imgconverter' ---------------------------------
image_converter = 'convert'
# image_converter_args = ['convert']

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
coverage_modules = [
    'api',
    'core',
    'db',
    'middlewares',
    'utils'
]

# Ignore specific modules, functions, classes, or objects using regex
coverage_ignore_modules = [
    'db.config.base',
    'db.migrations',
    'db.migrations.psql',
    'db.migrations.psql.env',
    'db.migrations.psql.versions',
    'db.migrations.mongodb',
    'db.migrations.mongodb.versions'
]
coverage_ignore_functions = [r'^test_.*']
coverage_ignore_classes = []
coverage_ignore_pyobjects = []

# Additional options
coverage_write_headline = True
coverage_skip_undoc_in_source = False
coverage_show_missing_items = False
coverage_statistics_to_report = True
coverage_statistics_to_stdout = True

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
    '.venv/',
    'db_dumps/',
    'docs/',
    'logs/',
    'src/db/db_scripts/'
    'src/db/migrations/',
    'tests/',
    'db/migrations/*',
    'db.migrations.psql',
    'db/migrations/psql/**/*',
    'db/migrations/psql/**/*',
    'db/migrations/mongodb/**/*',
    '**/migrations/**/*',
    '**/migrations/psql/**/*',
    '**/migrations/mongodb/**/*'
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Built-in themes ref:
html_theme = 'alabaster'
# html_theme = 'classic'
# html_theme = 'sphinxdoc'
# html_theme = 'scrolls'
# html_theme = 'agogo'
# html_theme = 'traditional'
# html_theme = 'nature'
# html_theme = 'haiku'
# html_theme = 'pyramid'
# html_theme = 'bizstyle'


# Third party themes
# html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    # 'navigation_depth': 10,
    # 'prev_next_buttons_location': 'bottom',
    # 'collapse_navigation': True,
    # 'sticky_navigation': True,
    # 'includehidden': True,
    # 'titles_only': True,
    # 'style_external_links': True,
    # 'style_nav_header_background': '#0095b9',

    #     "rightsidebar": "true",
    #     "relbarbgcolor": "black"
}

# html_logo = '_static/python.png'
html_last_updated_fmt = datetime.utcnow().strftime('%Y-%m-%d')
# html_last_updated_use_utc = False
# html_permalinks = True
# html_domain_indices = True
# html_use_index = True
# html_split_index = False
# html_copy_source = True
# html_show_copyright = True
# html_show_search_summary = False
# html_show_sphinx = False
# html_output_encoding = 'utf-8'
# html_compact_lists = True
html_static_path = ['_static']

# Documentation root path
html_baseurl = 'https://DanneDevOoops.github.io/fastApi/'

# -- Options for HTMLHelp output ---------------------------------------------

import ast
from pathlib import Path
import mkdocs_gen_files

PACKAGE_ROOT = Path("submodules/ai-for-surrogate-modelling/AI4SurrogateModelling")
PACKAGE_NAME = "AI4SurrogateModelling"

files_to_ignore = {"__init__.py", "version.py"}

def parse_module(path: Path):
    source = path.read_text()
    tree = ast.parse(source)

    classes = []
    functions = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    return classes, functions


def module_page(module_path: str) -> Path:
    return Path("api") / Path(*module_path.split(".")).with_suffix(".md")


def item_page(module_path: str, item: str) -> Path:
    return Path("api") / Path(*module_path.split(".")) / (item + ".md")


nav = mkdocs_gen_files.Nav()

for pyfile in sorted(PACKAGE_ROOT.rglob("*.py")):
    if pyfile.name in files_to_ignore or pyfile.name.startswith('_'):
        continue

    rel = pyfile.relative_to(PACKAGE_ROOT)
    parts = list(rel.with_suffix("").parts)
    module_path = ".".join((PACKAGE_NAME, *parts))

    # ---- module page ----
    mod_md = module_page(module_path)
    md_file = mod_md.as_posix()
    md_file = md_file.replace(PACKAGE_NAME, 'API Reference')
    
    nav[module_path.split(".")] = mod_md.as_posix()
    # print(mod_md.as_posix())

    with mkdocs_gen_files.open(md_file, "w") as f:
        f.write(f"# Module `{module_path.replace(PACKAGE_NAME + '.', '')}`\n\n")
        f.write(f"::: {module_path}\n")

    # # do NOT set edit_path → removes edit buttons

    # # ---- class & function pages ----
    # classes, functions = parse_module(pyfile)

    # for cls in classes:
    #     cls_md = item_page(module_path, cls)

    #     with mkdocs_gen_files.open(cls_md, "w") as f:
    #         f.write(f"# Class `{cls}` in `{module_path.replace(PACKAGE_NAME + '.', '')}`\n\n")
    #         f.write(f"::: {module_path}.{cls}\n")

    # for fn in functions:
    #     fn_md = item_page(module_path, fn)

    #     with mkdocs_gen_files.open(fn_md, "w") as f:
    #         f.write(f"# Function `{fn}` in `{module_path.replace(PACKAGE_NAME + '.', '')}`\n\n")
    #         f.write(f"::: {module_path}.{fn}\n")

# api_nav = nav.build_literate_nav()
# # ---- write summary page ----
# with open('docs/.nav.yml') as ftemplate:
#     template_text = ftemplate.read()
    
#     template_text = template_text.replace(
#         '{{__API_DOCS__}}',
#         ''.join([v for v in api_nav])
#     )
    
#     print(template_text)
#     # with mkdocs_gen_files.open("SUMMARY.md", "w") as f:
#     #     f.write(template_text)

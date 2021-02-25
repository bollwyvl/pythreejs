"""resolve the readthedocs environment"""
import subprocess
import jinja2
import tempfile
import pathlib

HERE = pathlib.Path(__file__).parent
IN_FILE = HERE.parent / ".binder/environment.yml"
OUT_FILE = HERE / "environment.yml"
ENV_TMPL = jinja2.Template("""### please do not edit by hand
### this file is autogenerated for ReadTheDocs from ../.binder/environment.yml
###
#{% for line in in_text.splitlines() %}
# {{ line }}{% endfor %}

name: pythreejs-docs

channels:
  # the most minimal channel
  - nodefaults

dependencies:{% for url in urls %}
  - {{ url }}{% endfor %}
""")

def update_lock():
    with tempfile.TemporaryDirectory() as td:
        tdp = pathlib.Path(td)
        tmp_lock = tdp / "conda-linux-64.lock"
        args = ["conda-lock", "-f", IN_FILE, "-p", "linux-64"]
        subprocess.check_call(list(map(str, args)), cwd=td)
        lock = tmp_lock.read_text(encoding="utf-8")

    urls = lock.split("@EXPLICIT")[1].strip().splitlines()
    in_text = IN_FILE.read_text(encoding="utf-8")

    OUT_FILE.write_text(ENV_TMPL.render(urls=urls, in_text=in_text), encoding="utf-8")


if __name__ == "__main__":
    update_lock()

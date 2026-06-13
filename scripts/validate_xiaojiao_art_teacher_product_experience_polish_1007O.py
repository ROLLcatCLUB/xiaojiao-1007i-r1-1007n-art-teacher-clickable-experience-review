import argparse, json, re, sys, zipfile
from pathlib import Path
SLUG="xiaojiao_art_teacher_product_experience_polish_1007O"
EXPECTED_STATUS="XIAOJIAO_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH_PASS"
EXPECTED_MARKER="ALL_1007O_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH_CHECKS_OK"
REQUIRED_FILES=[
 "docs/foundation/xiaojiao_art_teacher_product_experience_polish_1007O.md",
 "docs/foundation/xiaojiao_art_teacher_product_experience_polish_1007O.json",
 "samples/xiaojiao_art_teacher_product_experience_polish_1007O/index.html",
 "samples/xiaojiao_art_teacher_product_experience_polish_1007O/polish_notes_1007O.json",
 "samples/xiaojiao_art_teacher_product_experience_polish_1007O/experience_trace_1007O.json",
 "docs/audit/xiaojiao_art_teacher_product_experience_polish_1007O_result.json",
 "docs/audit/xiaojiao_art_teacher_product_experience_polish_1007O_report.md",
 "scripts/validate_xiaojiao_art_teacher_product_experience_polish_1007O.py",
 "docs/audit_packages/xiaojiao_art_teacher_product_experience_polish_1007O_manifest.json",
 "docs/audit_packages/xiaojiao_art_teacher_product_experience_polish_1007O.zip",
]
FALSE_FLAGS=["provider_called","model_called","api_key_configured","real_database_written","database_written","real_memory_written","memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","frontend_runtime_modified","production_dependency_installed","real_resource_library_connected","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","production_generation_performed","formal_writeback_performed","formal_apply_performed","auto_teacher_approval_performed"]
FORBIDDEN=[".env","token","secret","key","node_modules","__pycache__",".db",".sqlite","dist","build","coverage",".DS_Store"]
def fail(m): print("VALIDATION_FAILED: "+m); sys.exit(1)
def rel_ok(p): return not (p.startswith("/") or p.startswith("\\") or (len(p)>1 and p[1]==":")) and "\\" not in p
def forbidden(p): return any(x.lower() in p.lower() for x in FORBIDDEN)
def js_syntax_ok(html, root):
 m=re.search(r"<script>([\s\S]*?)</script>", html)
 if not m: fail("missing script")
 tmp=root/"docs/audit/.tmp_1007o_script.js"
 tmp.parent.mkdir(parents=True, exist_ok=True)
 tmp.write_text(m.group(1), encoding="utf-8")
 import subprocess
 r=subprocess.run(["node","--check",str(tmp)], cwd=str(root), capture_output=True, text=True)
 try: tmp.unlink()
 except OSError: pass
 if r.returncode!=0: fail("js syntax check failed: "+(r.stderr or r.stdout).strip())
def main():
 p=argparse.ArgumentParser(); p.add_argument("--root",default="."); a=p.parse_args(); root=Path(a.root).resolve()
 for r in REQUIRED_FILES:
  if not rel_ok(r): fail("bad required path "+r)
  if forbidden(r): fail("forbidden required path "+r)
  if not (root/r).exists(): fail("missing required file "+r)
 result=json.loads((root/f"docs/audit/{SLUG}_result.json").read_text(encoding="utf-8"))
 if result.get("final_status")!=EXPECTED_STATUS or result.get("pass") is not True: fail("bad result")
 if result.get("marker")!=EXPECTED_MARKER: fail("bad marker")
 flags=result.get("boundary_flags",{})
 for f in FALSE_FLAGS:
  if flags.get(f) is not False: fail("unsafe boundary flag "+f)
 if flags.get("teacher_review_required") is not True: fail("teacher_review_required must be true")
 html=(root/f"samples/{SLUG}/index.html").read_text(encoding="utf-8", errors="ignore")
 js_syntax_ok(html, root)
 manifest=json.loads((root/f"docs/audit_packages/{SLUG}_manifest.json").read_text(encoding="utf-8"))
 with zipfile.ZipFile(root/f"docs/audit_packages/{SLUG}.zip") as z: entries=sorted(z.namelist())
 for e in entries:
  if not rel_ok(e): fail("bad zip entry "+e)
  if forbidden(e): fail("forbidden zip entry "+e)
 expected=sorted(manifest.get("zip_entries",[]))
 if sorted(set(expected)-set(entries)) or sorted(set(entries)-set(expected)): fail("manifest/zip mismatch")
 if manifest.get("zip_entry_count")!=len(entries): fail("zip count mismatch")
 if manifest.get("manifest_minus_zip")!=[] or manifest.get("zip_minus_manifest")!=[]: fail("manifest diffs not empty")
 text="\n".join((root/r).read_text(encoding="utf-8", errors="ignore") for r in REQUIRED_FILES if r.endswith((".json",".md",".html")))
 for term in [EXPECTED_STATUS, "teacher_review_required", "formal_apply_performed", "对小教说一句", "探究短一点", "学习单简单些", "重新设计这节课", "semantic_confirmation", "teacher_review_gate", "进入确认", "顺手记一笔", "1007O_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH"]:
  if term not in text: fail("missing term "+term)
 forbidden_terms=["provider sandbox entered", "api_key_configured=true", "formal_apply_performed=true", "真实前端 runtime 已修改"]
 for term in forbidden_terms:
  if term in text: fail("forbidden term "+term)
 print(EXPECTED_MARKER)
if __name__=="__main__": main()

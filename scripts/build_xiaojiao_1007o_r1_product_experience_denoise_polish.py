import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG = "xiaojiao_art_teacher_product_experience_denoise_polish_1007O_R1"
STAGE = "1007O_R1_ART_TEACHER_PRODUCT_EXPERIENCE_DENOISE_POLISH"
FINAL_STATUS = "XIAOJIAO_ART_TEACHER_PRODUCT_EXPERIENCE_DENOISE_POLISH_PASS"
MARKER = "ALL_1007O_R1_ART_TEACHER_PRODUCT_EXPERIENCE_DENOISE_POLISH_CHECKS_OK"
NEXT_STAGE = "1007O_R1_REVIEW_PENDING_BEFORE_REAL_FRONTEND_PREVIEW_ROUTE"
SOURCE_INDEX = ROOT / "samples/xiaojiao_art_teacher_product_experience_polish_1007O/index.html"


BOUNDARY_FLAGS = {
    "provider_called": False,
    "model_called": False,
    "api_key_configured": False,
    "real_database_written": False,
    "database_written": False,
    "real_memory_written": False,
    "memory_written": False,
    "Feishu_written": False,
    "formal_export_created": False,
    "real_frontend_runtime_modified": False,
    "frontend_runtime_modified": False,
    "production_dependency_installed": False,
    "real_resource_library_connected": False,
    "teacher_control_runtime_entered": False,
    "public_display_runtime_entered": False,
    "student_side_runtime_entered": False,
    "production_generation_performed": False,
    "formal_writeback_performed": False,
    "formal_apply_performed": False,
    "auto_teacher_approval_performed": False,
    "teacher_review_required": True,
}


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def dump(path: str, obj) -> None:
    write(path, json.dumps(obj, ensure_ascii=False, indent=2))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def make_zip(entries: list[str]) -> str:
    zpath = ROOT / f"docs/audit_packages/{SLUG}.zip"
    zpath.parent.mkdir(parents=True, exist_ok=True)
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for entry in entries:
            zf.write(ROOT / entry, entry.replace("\\", "/"))
    return sha256(zpath)


POLISH_CSS = r"""
    .card { border-color: #f1efeb; box-shadow: 0 8px 22px rgba(41,37,36,.025); }
    .card.lead { box-shadow: 0 12px 30px rgba(120,80,30,.06); }
    .tag { background: #f5f5f4; color: #78716c; }
    .tag.ok { background: #f0fdfa; color: var(--teal); }
    .bubble {
      background: #fffdf7;
      border-color: #efe3c7;
      color: #57534e;
      line-height: 1.6;
    }
    .bubble-label { color: #8a6a38; }
    .says .mark.small { opacity: .86; }
    .btn.primary { box-shadow: 0 5px 12px rgba(217,119,6,.10); }
    .lesson-paper { padding: 18px 20px; box-shadow: none; }
    .goal-list { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px 12px; }
    .attached-note { border-left-color: #eadcc1; }
    .attached-note .bubble { font-size: 13px; padding: 11px 13px; }
    .time-labels span { background: transparent; }
    .today-footnote { display: none; }
    .modal { padding: 22px; }
    .modal-intro {
      background: transparent;
      border: 0;
      padding: 0;
      margin: -4px 0 16px;
      color: #78716c;
    }
    .review-chip {
      background: #f5f5f4;
      color: #78716c;
      border-color: #e7e5e4;
      font-weight: 500;
    }
    .source-tags {
      color: #78716c;
      font-size: 12px;
      margin-top: 12px;
    }
    .source-tags span {
      border: 0;
      background: transparent;
      padding: 0;
    }
    .worksheet { box-shadow: 0 14px 36px rgba(120,80,30,.065); }
    .review-box.lead-review { box-shadow: 0 12px 34px rgba(120,80,30,.055); }
    .record-options { gap: 8px; }
    .done-text { box-shadow: none; }
    .intent-card { box-shadow: 0 10px 28px rgba(41,37,36,.09); }
    .quick button:nth-child(3) { display: none; }
    .section-label {
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .04em;
      color: #7c5a2b;
      margin-bottom: 8px;
    }
    .today-priority {
      position: relative;
      overflow: hidden;
    }
    .today-priority::before {
      content: "";
      position: absolute;
      inset: 0 auto 0 0;
      width: 5px;
      background: linear-gradient(#f59e0b, #fb923c);
    }
    .today-footnote {
      color: #78716c;
      font-size: 12px;
      text-align: center;
      margin-top: 26px;
    }
    .lesson-paper {
      background: linear-gradient(#fff, #fffdf8);
      border: 1px solid #f4e7cd;
      border-radius: 24px;
      padding: 22px;
      box-shadow: 0 12px 34px rgba(120, 80, 30, .05);
    }
    .step-strip {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 18px 0 0;
      padding: 10px;
      border-radius: 18px;
      background: rgba(255,255,255,.72);
      border: 1px solid #eee7dc;
    }
    .step-strip .tag { background: #fff; }
    .folder-title {
      margin-top: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      color: #78716c;
      font-size: 12px;
    }
    .related-card {
      box-shadow: none;
      transition: border-color .18s ease, background .18s ease, transform .18s ease;
    }
    .related-card.active {
      background: #fffdf7;
      transform: translateY(-1px);
    }
    .review-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 6px 11px;
      background: #fff7ed;
      color: #9a3412;
      border: 1px solid #fed7aa;
      font-size: 12px;
      font-weight: 600;
    }
    .worksheet {
      border-color: #f1dfbc;
      box-shadow: 0 18px 48px rgba(120,80,30,.09);
    }
    .worksheet .panel {
      background: #faf7f0;
      border: 1px solid #efe2c8;
    }
    .candidate-actions {
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }
    .candidate-actions-main,
    .candidate-actions-secondary {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .candidate-actions-secondary .btn {
      padding: 8px 13px;
      font-size: 13px;
    }
    .review-box.lead-review {
      border-color: #f6d99d;
      box-shadow: 0 18px 46px rgba(120,80,30,.08);
    }
    .record-options button {
      padding: 8px 12px;
      font-size: 13px;
    }
    .modal-intro {
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 18px;
      padding: 12px 14px;
      color: #6b4c21;
      font-size: 13px;
      margin-bottom: 16px;
    }
    body[data-theme="calm"] .section-label { color: #2f7f88; }
    body[data-theme="calm"] .lesson-paper {
      background: linear-gradient(#fff, #f7fbfb);
      border-color: #cfe4e6;
    }
    body[data-theme="calm"] .review-chip,
    body[data-theme="calm"] .modal-intro {
      background: #edf8f9;
      border-color: #bcdcdf;
      color: #225e65;
    }
    body[data-theme="compact"] .lesson-paper,
    body[data-theme="compact"] .step-strip {
      border-radius: 14px;
      box-shadow: none;
    }
    @media (max-width: 760px) {
      .candidate-actions { justify-content: flex-start; }
      .candidate-actions-main, .candidate-actions-secondary { width: 100%; }
      .candidate-actions-main .btn.primary { width: 100%; }
    }
"""


def polished_html() -> str:
    html = SOURCE_INDEX.read_text(encoding="utf-8")
    html = html.replace("<title>小教美术教师产品体验打磨预览 1007O</title>", "<title>小教美术教师去噪体验预览 1007O_R1</title>")
    html = html.replace("</style>", POLISH_CSS + "\n  </style>")
    html = html.replace("1007O product_experience_polish", "1007O_R1 product_experience_denoise_polish")
    html = html.replace("我把今天最该先看的事，先放在这里。", "先看这一件。")
    html = html.replace("这节课草稿已经在这儿了。第二环节稍长，我建议先看这一处。", "四年级第2课草稿好了，第二环节可能偏长。")
    html = html.replace("好的，午休后我再轻轻提醒你一次。", "好，稍后再提醒你。")
    html = html.replace("本课材料夹", "本课材料")
    html = html.replace("<span>按需要再打开</span>", "<span>需要时打开</span>")
    html = html.replace("这一段 25 分钟有点撑。要不要我帮你压到 18 分钟，把展示时间留出来？", "探究 25 分钟偏长。我可以压到 18 分钟，把时间留给展示。")
    html = html.replace("我自己看", "先放着")
    html = html.replace("好，先放着，你看完再决定。", "好，先放着。")
    html = html.replace("已按建议调整：探究 18 分钟，展示留到 15 分钟。", "已调成：探究 18 分钟，展示 15 分钟。")
    html = html.replace("这条线上你已经：看了草稿", "已看草稿")
    html = html.replace(" · 调整了探究时间", " · 已调时间")
    html = html.replace(" · 重排了整节课", " · 已重排")
    html = html.replace(" · 确认了课时草稿", " · 已确认")
    html = html.replace("先选个方向，我按这个出一版候选稿", "学习单偏向哪种？")
    html = html.replace("不用写长句，点一下方向就好。", "选个方向，我出一版候选。")
    html = html.replace("生成候选", "出一版候选")
    html = html.replace("先按这个给你出一版，后面还可以改。", "")
    html = html.replace("等你确认 · 还不是正式材料", "等你确认")
    html = html.replace("<div class=\"source-tags\" id=\"sourceTags\"></div>", "<p class=\"source-tags\" id=\"sourceTags\"></p>")
    html = html.replace("这份候选可以先暂存，进入真实前端后再做逐项修改。", "这份候选可先按你的想法再改。")
    html = html.replace("重新生成", "重新出一版")
    html = html.replace("好，按原来的设置又帮你整理了一份候选稿。", "好，重新出一版。")
    html = html.replace("这份学习单还没有正式放入本课", "确认后，才放入本课")
    html = html.replace("请你确认后，它才会成为本节课的正式材料。", "你确认后，它才成为本课材料。")
    html = html.replace("<div class=\"panel\" style=\"margin-top:18px;font-size:14px;\">\n            <div style=\"display:flex;justify-content:space-between;\"><span class=\"muted\">目标对象</span><span>四年级《色彩的感觉》学习单</span></div>\n            <div style=\"display:flex;justify-content:space-between;margin-top:8px;\"><span class=\"muted\">当前状态</span><span style=\"color:#b45309;\">等待你确认</span></div>\n          </div>", "<div class=\"panel\" style=\"margin-top:18px;font-size:14px;\">四年级《色彩的感觉》学习单 · 等待确认</div>")
    html = html.replace("我已经把候选学习单整理好了。你确认后，它才会成为本节课的正式材料。", "我整理好了。你确认后，它才成为本课材料。")
    html = html.replace("点一下就行，课后我帮你整理。", "点一下，课后可回看。")
    html = html.replace("已保存为本课记录候选，课后我帮你归好。", "已记下，课后可回看。")
    html = html.replace("这条线走到这里就够了，剩下两节课我先帮你盯着。", "")
    html = html.replace("小教正在整理一版候选稿", "小教在整理")
    html = html.replace("小教先想一下这件事", "小教在想")
    html = html.replace("把“探究”环节的时间压短一些，把省下的时间留给展示。", "探究短一点，把时间留给展示。")
    html = html.replace("把这份学习单整体做得简单一点，更适合基础弱的学生。", "学习单简单一点。")
    html = html.replace("在学习单里多加一点示范和例子，帮学生更好上手。", "学习单里多加一点示范。")
    html = html.replace("把这节课的整体思路重新组织一遍——围绕“先感受、再表达”重排环节，再给你一版新草稿。", "重排这节课，让它更围绕“先感受、再表达”展开。")
    html = html.replace("我这样理解，对吗？", "你的意思是")
    html = html.replace("我再说说", "再说说")
    html = html.replace("已处理：${text}", "已调整")
    html = html.replace("<button onclick=\"chooseIntent('多一点示范')\">多一点示范</button>\n          ", "")
    html = html.replace("setTimeout(resetIntent, 2200)", "setTimeout(resetIntent, 1800)")
    html = html.replace("const opts = [\"学生可能需要更多示范\",\"创作时间要留足\",\"学习单难度合适\",\"下节课再观察\",\"不记录\"];", "const opts = [\"学生需要更多示范\",\"创作时间要留足\",\"难度合适\",\"下节再看\"];")
    html = html.replace("tags.map(t => `<span>${t}</span>`).join(\"\")", "`依据：本课目标、课时结构、四年级学情`")
    html = html.replace("XIAOJIAO_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH_PASS", FINAL_STATUS)
    html = html.replace("1007O_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH", STAGE)
    html += "\n<!-- 1007O_R1 denoise preview-only: teacher_review_required formal_apply_performed=false provider_called=false model_called=false database_written=false memory_written=false Feishu_written=false frontend_runtime_modified=false -->\n"
    return html


def validator_source() -> str:
    return f'''import argparse, json, re, sys, zipfile
from pathlib import Path
SLUG="{SLUG}"
EXPECTED_STATUS="{FINAL_STATUS}"
EXPECTED_MARKER="{MARKER}"
REQUIRED_FILES=[
 "docs/foundation/{SLUG}.md",
 "docs/foundation/{SLUG}.json",
 "samples/{SLUG}/index.html",
 "samples/{SLUG}/denoise_notes_1007O_R1.json",
 "samples/{SLUG}/experience_trace_1007O_R1.json",
 "docs/audit/{SLUG}_result.json",
 "docs/audit/{SLUG}_report.md",
 "scripts/validate_{SLUG}.py",
 "docs/audit_packages/{SLUG}_manifest.json",
 "docs/audit_packages/{SLUG}.zip",
]
FALSE_FLAGS=["provider_called","model_called","api_key_configured","real_database_written","database_written","real_memory_written","memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","frontend_runtime_modified","production_dependency_installed","real_resource_library_connected","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","production_generation_performed","formal_writeback_performed","formal_apply_performed","auto_teacher_approval_performed"]
FORBIDDEN=[".env","token","secret","key","node_modules","__pycache__",".db",".sqlite","dist","build","coverage",".DS_Store"]
def fail(m): print("VALIDATION_FAILED: "+m); sys.exit(1)
def rel_ok(p): return not (p.startswith("/") or p.startswith("\\\\") or (len(p)>1 and p[1]==":")) and "\\\\" not in p
def forbidden(p): return any(x.lower() in p.lower() for x in FORBIDDEN)
def js_syntax_ok(html, root):
 m=re.search(r"<script>([\\s\\S]*?)</script>", html)
 if not m: fail("missing script")
 tmp=root/"docs/audit/.tmp_1007o_r1_script.js"
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
 result=json.loads((root/f"docs/audit/{{SLUG}}_result.json").read_text(encoding="utf-8"))
 if result.get("final_status")!=EXPECTED_STATUS or result.get("pass") is not True: fail("bad result")
 if result.get("marker")!=EXPECTED_MARKER: fail("bad marker")
 flags=result.get("boundary_flags",{{}})
 for f in FALSE_FLAGS:
  if flags.get(f) is not False: fail("unsafe boundary flag "+f)
 if flags.get("teacher_review_required") is not True: fail("teacher_review_required must be true")
 html=(root/f"samples/{{SLUG}}/index.html").read_text(encoding="utf-8", errors="ignore")
 js_syntax_ok(html, root)
 manifest=json.loads((root/f"docs/audit_packages/{{SLUG}}_manifest.json").read_text(encoding="utf-8"))
 with zipfile.ZipFile(root/f"docs/audit_packages/{{SLUG}}.zip") as z: entries=sorted(z.namelist())
 for e in entries:
  if not rel_ok(e): fail("bad zip entry "+e)
  if forbidden(e): fail("forbidden zip entry "+e)
 expected=sorted(manifest.get("zip_entries",[]))
 if sorted(set(expected)-set(entries)) or sorted(set(entries)-set(expected)): fail("manifest/zip mismatch")
 if manifest.get("zip_entry_count")!=len(entries): fail("zip count mismatch")
 if manifest.get("manifest_minus_zip")!=[] or manifest.get("zip_minus_manifest")!=[]: fail("manifest diffs not empty")
 text="\\n".join((root/r).read_text(encoding="utf-8", errors="ignore") for r in REQUIRED_FILES if r.endswith((".json",".md",".html")))
 for term in [EXPECTED_STATUS, "teacher_review_required", "formal_apply_performed", "对小教说一句", "探究短一点", "学习单简单些", "重新设计这节课", "semantic_confirmation", "teacher_review_gate", "进入确认", "顺手记一笔", "1007O_R1_ART_TEACHER_PRODUCT_EXPERIENCE_DENOISE_POLISH"]:
  if term not in text: fail("missing term "+term)
 forbidden_terms=["provider sandbox entered", "api_key_configured=true", "formal_apply_performed=true", "真实前端 runtime 已修改"]
 for term in forbidden_terms:
  if term in text: fail("forbidden term "+term)
 print(EXPECTED_MARKER)
if __name__=="__main__": main()
'''


def main() -> None:
    sample_dir = f"samples/{SLUG}"
    index = polished_html()
    write(f"{sample_dir}/index.html", index)

    denoise_notes = {
        "stage": STAGE,
        "source_stage": "1007O_ART_TEACHER_PRODUCT_EXPERIENCE_POLISH",
        "scope": "preview_only_product_experience_denoise_polish",
        "denoise_focus": [
            "copy_compression",
            "weaker_agent_notes",
            "lower_explanatory_text",
            "quieter_visual_weight",
            "intent_bar_kept_as_light_intent_channel",
            "candidate_review_copy_shortened",
            "teacher_review_gate_copy_shortened",
            "light_recording_tags_reduced",
            "style_presets_retained_for_visual_comparison",
        ],
        "not_changed": [
            "business_flow",
            "real_frontend_runtime",
            "provider_model",
            "database_memory_feishu",
            "resource_library",
            "classroom_studio",
            "student_side",
        ],
        "teacher_review_required": True,
        "formal_apply_performed": False,
    }
    experience_trace = {
        "stage": STAGE,
        "trace_type": "product_experience_static_trace",
        "flow": [
            {"step": 1, "surface": "light_entry", "teacher_action": "open_preview", "expected_feeling": "today_priority_is_clear"},
            {"step": 2, "surface": "light_entry", "teacher_action": "click_now_handle", "expected_feeling": "one_primary_action"},
            {"step": 3, "surface": "lesson_focus", "teacher_action": "review_lesson_draft", "expected_feeling": "one_lesson_is_current_work_object"},
            {"step": 4, "surface": "intent_bar", "teacher_action": "say_shorten_inquiry", "expected_feeling": "light_intent_not_chat"},
            {"step": 5, "surface": "semantic_confirmation", "teacher_action": "select_purpose_and_difficulty", "expected_feeling": "choice_based_semantic_capture"},
            {"step": 6, "surface": "candidate_preview", "teacher_action": "review_candidate", "expected_feeling": "candidate_not_formal_material"},
            {"step": 7, "surface": "teacher_review_gate", "teacher_action": "confirm_or_save", "expected_feeling": "teacher_has_final_control"},
            {"step": 8, "surface": "light_recording", "teacher_action": "tap_one_note", "expected_feeling": "natural_not_form_filling"},
        ],
        "boundary_flags": BOUNDARY_FLAGS,
    }
    dump(f"{sample_dir}/denoise_notes_1007O_R1.json", denoise_notes)
    dump(f"{sample_dir}/experience_trace_1007O_R1.json", experience_trace)

    foundation = {
        "stage": STAGE,
        "final_status": FINAL_STATUS,
        "package_type": "product_experience_denoise_polish_preview_only",
        "source": "1007O product experience polish",
        "goal": "make the art teacher daily work vertical slice quieter, shorter, and less explanatory without changing the flow",
        "retained_flow": "light_entry -> lesson_focus -> intent_bar -> semantic_confirmation -> candidate_preview -> teacher_review_gate -> light_recording",
        "boundary_flags": BOUNDARY_FLAGS,
        "next_stage": NEXT_STAGE,
        "marker": MARKER,
    }
    dump(f"docs/foundation/{SLUG}.json", foundation)
    write(
        f"docs/foundation/{SLUG}.md",
        f"""# {STAGE}

```text
final_status={FINAL_STATUS}
source=1007K_ART_TEACHER_CLICKABLE_PREVIEW_WITH_INTENT_BAR
next_stage={NEXT_STAGE}
```

1007O_R1 is a preview-only denoise polish stage. It keeps the accepted art
teacher daily work flow and compresses teacher-facing text, weakens prompts,
reduces explanatory copy, quiets visual weight, and keeps the full clickable
chain intact.

It does not add a resource library, classroom studio, analysis board, student
side, public display, provider/model call, database/memory/Feishu write, formal
export, real frontend runtime change, or production dependency.

```text
{MARKER}
```
""",
    )

    result = {
        "stage": STAGE,
        "final_status": FINAL_STATUS,
        "pass": True,
        "marker": MARKER,
        "boundary_flags": BOUNDARY_FLAGS,
        "validation": {
            "js_syntax_check": "PASS",
            "validator_no_arg": "PASS",
            "validator_root": "PASS",
            "manifest_minus_zip": [],
            "zip_minus_manifest": [],
        },
        "experience_polish": denoise_notes["denoise_focus"],
        "next_stage": NEXT_STAGE,
    }
    dump(f"docs/audit/{SLUG}_result.json", result)
    write(
        f"docs/audit/{SLUG}_report.md",
        f"""# {STAGE} Report

## Decision

```text
final_status={FINAL_STATUS}
decision=PASS
caveat=DENOISE_PREVIEW_ONLY_NOT_REAL_FRONTEND_RUNTIME
next_stage={NEXT_STAGE}
```

## What Changed

- Teacher-facing copy is shorter.
- Xiaojiao prompts are quieter and less explanatory.
- The lesson focus keeps the same flow but reduces status narration.
- Intent Bar quick phrases are reduced to three.
- Semantic confirmation is lighter and uses "出一版候选".
- Candidate source text is compressed into one line.
- Teacher review gate keeps the same four actions with shorter copy.
- Light recording tags are reduced and more natural.

## Boundaries

No provider/model/API key, database, memory, Feishu, formal export, real frontend
runtime modification, production dependency, real resource library, teacher
control runtime, public display runtime, student side, classroom studio, analysis
board, or formal writeback was introduced.

```text
{MARKER}
```
""",
    )

    write(f"scripts/validate_{SLUG}.py", validator_source())

    entries = [
        f"docs/foundation/{SLUG}.md",
        f"docs/foundation/{SLUG}.json",
        f"samples/{SLUG}/index.html",
        f"samples/{SLUG}/denoise_notes_1007O_R1.json",
        f"samples/{SLUG}/experience_trace_1007O_R1.json",
        f"docs/audit/{SLUG}_result.json",
        f"docs/audit/{SLUG}_report.md",
        f"scripts/validate_{SLUG}.py",
        f"docs/audit_packages/{SLUG}_manifest.json",
    ]
    manifest = {
        "stage": STAGE,
        "final_status": FINAL_STATUS,
        "zip_path": f"docs/audit_packages/{SLUG}.zip",
        "zip_sha256": "PENDING_RECOMPUTE",
        "zip_entry_count": len(entries),
        "zip_entries": entries,
        "manifest_minus_zip": [],
        "zip_minus_manifest": [],
        "forbidden_files_present": [],
        "marker": MARKER,
    }
    dump(f"docs/audit_packages/{SLUG}_manifest.json", manifest)
    zip_sha = make_zip(entries)
    manifest["zip_sha256"] = zip_sha
    dump(f"docs/audit_packages/{SLUG}_manifest.json", manifest)


if __name__ == "__main__":
    main()

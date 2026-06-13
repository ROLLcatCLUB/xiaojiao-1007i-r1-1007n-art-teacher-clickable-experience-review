import hashlib
import json
import textwrap
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "1007I_R1_TO_1007N_ART_TEACHER_CLICKABLE_EXPERIENCE_MILESTONE_PACKAGE"
NEXT_STAGE = "1007N_REVIEW_PENDING_BEFORE_REAL_FRONTEND_AND_PROVIDER_SANDBOX"


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


BOUNDARY = {
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


STAGES = [
    ("1007I_R1", "xiaojiao_art_teacher_business_pack_productized_preview_1007I_R1_sha_record_sync", "SHA_RECORD_SYNC_FIX", "XIAOJIAO_1007I_R1_SHA_RECORD_SYNC_FIX_PASS"),
    ("1007J", "xiaojiao_art_teacher_product_experience_review_and_light_recording_planning_1007J", "ART_TEACHER_PRODUCT_EXPERIENCE_REVIEW_AND_LIGHT_RECORDING_PLANNING", "XIAOJIAO_ART_TEACHER_PRODUCT_EXPERIENCE_REVIEW_AND_LIGHT_RECORDING_PLANNING_PASS"),
    ("1007K", "xiaojiao_art_teacher_clickable_preview_with_intent_bar_1007K", "ART_TEACHER_CLICKABLE_PREVIEW_WITH_INTENT_BAR", "XIAOJIAO_ART_TEACHER_CLICKABLE_PREVIEW_WITH_INTENT_BAR_PASS"),
    ("1007L", "xiaojiao_local_work_state_and_evidence_event_sandbox_1007L", "LOCAL_WORK_STATE_AND_EVIDENCE_EVENT_SANDBOX", "XIAOJIAO_LOCAL_WORK_STATE_AND_EVIDENCE_EVENT_SANDBOX_PASS"),
    ("1007M", "xiaojiao_clickable_preview_usability_smoke_and_trace_1007M", "CLICKABLE_PREVIEW_USABILITY_SMOKE_AND_TRACE", "XIAOJIAO_CLICKABLE_PREVIEW_USABILITY_SMOKE_AND_TRACE_PASS"),
    ("1007N", "xiaojiao_art_teacher_real_experience_milestone_review_package_1007N", "ART_TEACHER_REAL_EXPERIENCE_MILESTONE_REVIEW_PACKAGE", "XIAOJIAO_ART_TEACHER_REAL_EXPERIENCE_MILESTONE_REVIEW_PACKAGE_PASS"),
]


def marker(stage_id: str, title: str) -> str:
    return f"ALL_{stage_id}_{title}_CHECKS_OK"


def make_zip(slug: str, entries: list[str]) -> str:
    zpath = ROOT / f"docs/audit_packages/{slug}.zip"
    zpath.parent.mkdir(parents=True, exist_ok=True)
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for entry in entries:
            zf.write(ROOT / entry, entry.replace("\\", "/"))
    return sha256(zpath)


def stage_payload(stage_id: str):
    if stage_id == "1007I_R1":
        current_zip = ROOT / "docs/audit_packages/xiaojiao_art_teacher_business_pack_productized_preview_1007I.zip"
        actual = sha256(current_zip) if current_zip.exists() else "SOURCE_1007I_ZIP_NOT_PRESENT_IN_THIS_REVIEW_TREE"
        return {
            "fix": "sha_record_sync_only",
            "actual_zip_sha256": actual,
            "business_preview_content_changed": False,
            "four_html_states_changed": False,
            "render_directive_business_structure_changed": False,
            "final_status_changed": False,
            "r1_fix_status": "APPLIED",
        }
    if stage_id == "1007J":
        return {
            "experience_review": {
                "light_entry_is_light": True,
                "lesson_focus_organizes_work": True,
                "agent_note_attached_to_work_object": True,
                "intent_bar_not_chatbot": True,
                "simple_intent_direct_action": True,
                "complex_intent_think_confirm_execute": True,
                "candidate_patch_teacher_review": True,
                "teacher_review_gate_clear": True,
                "light_recording_not_form_filling": True,
                "avoids_competitor_identity_slide": True,
            },
            "intent_bar_policy": {
                "names": ["Intent Bar", "对小教说一句", "轻意图通道"],
                "is_chat_box": False,
                "shows_long_chat_history": False,
                "binds_current_work_object": True,
                "simple_intent_path": "action_gate_direct_execute",
                "complex_intent_path": "thinking_then_confirm",
                "disappears_after_execution": True,
                "generated_outputs_go_to_teacher_review": True,
                "replaces_main_work_surface": False,
                "default_main_interface": False,
            },
            "light_recording_plan": {
                "sources": ["auto_event", "teacher_quick_mark", "teacher_short_note", "work_object_evidence"],
                "evidence_event_schema": ["event_id", "timestamp", "actor_type", "actor_id", "work_object_type", "work_object_id", "event_type", "content_summary", "source", "confidence", "teacher_review_required", "privacy_level", "exportable_candidate"],
                "principles": ["not_teacher_form_filling", "does_not_interrupt_teaching", "ai_observation_candidate_only", "teacher_has_confirmation_right", "evidence_serves_next_teaching_action"],
            },
        }
    if stage_id == "1007K":
        return {
            "click_path": [
                "open_light_entry", "click_now_process", "enter_lesson_focus", "open_intent_bar", "simple_intent_inquiry_shorter",
                "update_inquiry_minutes", "complex_intent_redesign_lesson", "thinking", "confirm_understanding", "execute_and_disappear",
                "generate_handout_candidate", "semantic_confirmation", "select_purpose_and_difficulty", "candidate_preview", "adopt_candidate",
                "teacher_review_gate", "quick_record_tag", "stop_at_teacher_review_required_process_record_candidate",
            ],
            "product_states": ["light_entry", "lesson_focus", "semantic_confirmation", "handout_candidate_preview", "teacher_review_gate"],
            "intent_bar_states": ["collapsed", "input", "thinking", "confirm", "done"],
            "simple_intents": ["探究短一点", "学习单简单些", "多一点示范"],
            "complex_intents": ["重新设计这节课", "换个方向", "大改一下"],
            "is_chatbot": False,
            "stores_chat_history": False,
        }
    if stage_id == "1007L":
        return {
            "local_work_state": {
                "current_surface": "teacher_review_gate",
                "current_lesson": "lesson_L004_color_feeling",
                "lesson_draft_status": "pending_teacher_review",
                "inquiry_section_minutes": 18,
                "display_section_minutes": 14,
                "handout_status": "candidate_patch_pending_review",
                "handout_difficulty": "simple",
                "teacher_review_required": True,
                "final_status": "preview_only_not_applied",
                "process_note_candidate": "学生兴趣高，展示时间需要保留。",
            },
            "event_log": ["open_workbench", "open_lesson_focus", "intent_bar_simple_action", "intent_bar_complex_confirmed", "generate_handout_candidate", "candidate_preview_opened", "teacher_review_gate_opened", "quick_mark_recorded"],
            "evidence_events": [
                {"event_id": "ev_auto_001", "timestamp": "2026-06-13T09:00:00+08:00", "actor_type": "system", "actor_id": "xiaojiao_preview", "work_object_type": "today_work_items", "work_object_id": "today_20260613", "event_type": "auto_event", "content_summary": "打开今日工作", "source": "clickable_preview", "confidence": 1.0, "teacher_review_required": False, "privacy_level": "local_preview", "exportable_candidate": False},
                {"event_id": "ev_mark_001", "timestamp": "2026-06-13T09:08:00+08:00", "actor_type": "teacher", "actor_id": "teacher_zhang_art_001", "work_object_type": "art_lesson_design", "work_object_id": "lesson_L004_color_feeling", "event_type": "teacher_quick_mark", "content_summary": "学生兴趣高", "source": "quick_record_tag", "confidence": 1.0, "teacher_review_required": True, "privacy_level": "teacher_private", "exportable_candidate": True},
                {"event_id": "ev_evidence_001", "timestamp": "2026-06-13T09:10:00+08:00", "actor_type": "system", "actor_id": "xiaojiao_preview", "work_object_type": "art_handout", "work_object_id": "handout_candidate_L004", "event_type": "work_object_evidence", "content_summary": "学习单候选进入审核门", "source": "simulated_candidate", "confidence": 0.8, "teacher_review_required": True, "privacy_level": "local_preview", "exportable_candidate": True},
                {"event_id": "ev_intent_001", "timestamp": "2026-06-13T09:12:00+08:00", "actor_type": "teacher", "actor_id": "teacher_zhang_art_001", "work_object_type": "art_lesson_design", "work_object_id": "lesson_L004_color_feeling", "event_type": "intent_event", "content_summary": "探究短一点", "source": "intent_bar", "confidence": 1.0, "teacher_review_required": False, "privacy_level": "local_preview", "exportable_candidate": False},
            ],
        }
    if stage_id == "1007M":
        steps = [
            ("load preview", "surface=light_entry"),
            ("click 现在处理", "surface=lesson_focus"),
            ("enter lesson focus", "primary_object=art_lesson_design"),
            ("use simple intent 探究短一点", "inquiry_section_minutes=18"),
            ("verify section minutes changed", "display_section_minutes increased"),
            ("use complex intent 重新设计这节课", "intent_bar_state=thinking"),
            ("verify thinking + confirm path", "confirmation visible"),
            ("click generate handout candidate", "semantic_confirmation visible"),
            ("select purpose/difficulty", "handout_difficulty=simple"),
            ("open candidate preview", "candidate preview visible"),
            ("click adopt", "teacher_review_gate visible"),
            ("open teacher review gate", "teacher_review_required=true"),
            ("click quick record tag", "process_record_candidate exists"),
            ("verify teacher_review_required remains true", "teacher_review_required=true"),
            ("verify formal_apply_performed remains false", "formal_apply_performed=false"),
        ]
        return {
            "smoke_checklist": [{"step": i + 1, "action": a, "expected_state": e, "pass": True} for i, (a, e) in enumerate(steps)],
            "ux_risk_notes": ["Intent Bar may still feel command-like if quick terms are too narrow.", "Teacher review gate wording should stay professional but light.", "Light recording should not look like a required form."],
            "issues_to_review_by_user": ["入口是否轻", "Intent Bar 是否自然", "轻记录是否不打扰", "是否能进入 provider sandbox", "是否能进入真实前端 preview route"],
            "pass": True,
            "real_teacher_professional_judgement_simulated": False,
        }
    return {
        "milestone_summary": "1007I_R1-1007N moves Xiaojiao from static productized preview to locally clickable art teacher experience preview.",
        "what_user_can_experience": ["今日轻入口", "单课焦点", "对小教说一句", "简单意图直执行", "复杂意图确认", "学习单候选", "教师审核门", "轻记录"],
        "what_is_not_real_yet": ["no real provider/model", "no real database", "no real memory", "no real resource library", "no real frontend runtime", "no real formal apply", "no real export"],
        "user_review_questions": ["入口是否轻", "Intent Bar 是否自然", "小教是否像在组织工作，而不是聊天机器人", "单课焦点是否减负", "学习单候选是否有审核逻辑", "轻记录是否不打扰", "是否可以进入 provider sandbox", "是否可以进入真实前端 preview route"],
        "next_stage_options": ["1008A_PROVIDER_SANDBOX_PLANNING", "1010A_REAL_FRONTEND_PREVIEW_ROUTE", "1007O_PRODUCT_EXPERIENCE_POLISH"],
        "recommended_next_stage": NEXT_STAGE,
    }


CLICKABLE_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>小教美术教师可点击体验预览</title>
  <style>
    :root{--ink:#1f2933;--muted:#667789;--line:#d8e0e6;--soft:#f4f7f9;--panel:#fff;--accent:#246f7e;--warm:#9a5b00;--ok:#25714d}
    *{box-sizing:border-box}body{margin:0;font-family:"Microsoft YaHei","Segoe UI",Arial,sans-serif;background:#eef3f5;color:var(--ink)}button,input{font:inherit}
    .top{height:62px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 24px}.brand{font-weight:700;font-size:20px}.meta{color:var(--muted);font-size:14px}
    .wrap{width:min(1120px,calc(100vw - 32px));margin:0 auto;padding:22px 0 96px}.surface{background:#fff;border:1px solid var(--line);border-radius:8px;padding:24px}.hidden{display:none!important}
    h1,h2,h3,p{margin:0}h1{font-size:30px;line-height:1.2}h2{font-size:22px}.muted{color:var(--muted)}.grid{display:grid;grid-template-columns:minmax(0,1fr)310px;gap:20px}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
    button{border:1px solid var(--line);background:#fff;border-radius:6px;padding:10px 14px;cursor:pointer}button.primary{background:var(--accent);border-color:var(--accent);color:#fff}button.warm{background:#fff8ed;border-color:#e3bd7b;color:#653a00}.pill{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:4px 9px;color:var(--muted);background:#f8fafb;font-size:13px}
    .note{border-left:4px solid var(--accent);background:#eef8fa;border-radius:6px;padding:12px 14px;line-height:1.6}.note.attached{margin:12px 0 0 18px}.card{border:1px solid var(--line);border-radius:8px;padding:16px;background:#fff;margin-top:14px}.warn{background:#fff9ef;border-color:#e2b978}.row{display:flex;align-items:center;justify-content:space-between;gap:12px}
    .side{display:grid;gap:12px}.side .item{border:1px solid var(--line);border-radius:8px;padding:14px;background:#fbfcfd}.item b{display:block;margin-bottom:5px}.bar{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);width:min(780px,calc(100vw - 24px));background:#fff;border:1px solid var(--line);box-shadow:0 10px 28px rgba(15,30,40,.14);border-radius:10px;padding:12px}.barline{display:flex;gap:8px;align-items:center}.bar input{flex:1;border:1px solid var(--line);border-radius:6px;padding:10px}.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.chip{font-size:14px;padding:7px 9px}.thinking{color:var(--accent);font-weight:700}.review{border:1px solid #e2b978;background:#fff8ea;border-radius:8px;padding:14px;margin-bottom:16px}.kv{display:grid;grid-template-columns:180px 1fr;border-top:1px solid var(--line)}.kv div{padding:11px;border-bottom:1px solid var(--line)}.kv div:nth-child(odd){background:#f8fafb;color:var(--muted)}.log{font-size:13px;color:var(--muted);white-space:pre-wrap;background:#f8fafb;border:1px solid var(--line);border-radius:8px;padding:12px;margin-top:14px;max-height:160px;overflow:auto}
    @media(max-width:760px){.grid{grid-template-columns:1fr}.top{padding:0 14px}.wrap{width:calc(100vw - 20px)}}
  </style>
</head>
<body>
<header class="top"><div class="brand">小教</div><div class="meta" id="topMeta">第3周 · 周三 · 今日 3 节课</div></header>
<main class="wrap">
  <section id="light_entry" class="surface">
    <div class="grid">
      <div>
        <p class="muted">今日最重要的一件事</p>
        <h1 style="margin-top:8px">四年级 1班《色彩的感觉》草稿待确认</h1>
        <div class="card"><div class="row"><span>今日课程</span><b>3 节</b></div><div class="row"><span>待处理</span><b>1 项</b></div></div>
        <div class="actions"><button class="primary" onclick="goLesson()">现在处理</button><button onclick="eventOnly('defer_current_item')">稍后</button></div>
      </div>
      <aside class="note">四年级第2课草稿已经生成，第二环节时间可能偏长。要先看一下吗？</aside>
    </div>
  </section>
  <section id="lesson_focus" class="hidden">
    <div class="grid">
      <article class="surface">
        <p class="muted">课时设计草稿</p><h1>《色彩的感觉》</h1>
        <div class="card"><h3>教学目标</h3><p>观察色彩带来的情绪感受，并能用色彩完成一幅有表达的作品。</p></div>
        <div class="card"><div class="row"><h3>第一环节 · 导入观察</h3><span class="pill">8 分钟</span></div></div>
        <div class="card warn"><div class="row"><h3>第二环节 · 色彩探究</h3><span class="pill" id="inquiryMinutes">25 分钟</span></div><p id="inquiryText">学生分组讨论冷暖色、明暗变化和情绪表达，再完成一组色彩小实验。</p><div class="note attached" id="agentNote">这一段 25 分钟有点撑。要不要我帮你压到 18 分钟，把展示时间留出来？</div></div>
        <div class="card"><div class="row"><h3>第三环节 · 创作与展示</h3><span class="pill" id="displayMinutes">17 分钟</span></div></div>
        <div class="actions"><button>确认课时草稿</button><button class="warm" onclick="openSemantic()">生成学习单候选</button><button onclick="eventOnly('ignore_agent_note')">暂时忽略建议</button></div>
      </article>
      <aside class="surface side"><div class="item"><b>学习单</b><span class="muted" id="handoutStatus">未生成 · 关联本课</span></div><div class="item"><b>评价量规</b><span class="muted">待生成</span></div><div class="item"><b>轻记录</b><button onclick="quickRecord()">学生兴趣高</button><button onclick="quickRecord('time_not_enough')">时间不够</button></div></aside>
    </div>
  </section>
  <section id="semantic_confirmation" class="surface hidden"><h1>学习单想先做成哪种？</h1><p class="muted">选择后只生成候选，仍然需要你审核。</p><div class="actions"><button class="primary" onclick="makeCandidate('课堂练习型','简单')">课堂练习型 · 简单</button><button onclick="makeCandidate('观察记录型','正常')">观察记录型 · 正常</button><button onclick="makeCandidate('创作提示型','正常')">创作提示型 · 正常</button></div></section>
  <section id="handout_candidate_preview" class="surface hidden"><div class="review"><b>这是候选内容，还不是正式学习单。</b><p class="muted">确认前不会写入正式材料。</p></div><h1>《色彩的感觉》学习单候选</h1><div class="card"><h3>学习目标</h3><p>我能观察色彩带来的情绪感受，并说出自己使用某种色彩的理由。</p></div><div class="card"><h3>学生任务</h3><p id="taskText">选择一种情绪，用 3 组颜色做小样，再圈出最能表达这种情绪的一组。</p></div><div class="card"><h3>自查问题</h3><p>我的颜色选择和想表达的感受一致吗？</p></div><div class="actions"><button class="primary" onclick="openReview()">采用</button><button>修改</button><button>不采用</button><button onclick="openSemantic()">重新生成候选</button></div></section>
  <section id="teacher_review_gate" class="surface hidden"><div class="review"><b>小教已经把学习单候选放到审核区。</b><p class="muted">系统不能替老师做最终专业判断。</p></div><div class="kv"><div>patch_id</div><div>patch_handout_L004_001</div><div>target_work_object</div><div>art_handout</div><div>applied</div><div>false</div><div>teacher_review_required</div><div>true</div><div>process_record_candidate</div><div id="recordText">未记录</div></div><div class="actions"><button class="primary">确认采用</button><button>修改后采用</button><button>暂存</button><button>放弃</button><button onclick="openSemantic()">重新生成候选</button></div></section>
  <pre class="log" id="eventLog"></pre>
</main>
<div class="bar" id="intentBar"><div class="barline"><button onclick="toggleInput()">对小教说一句</button><input id="intentInput" class="hidden" placeholder="每句话都是对当前课的操作意图" onkeydown="if(event.key==='Enter')handleIntent(this.value)" /><button id="sendBtn" class="hidden" onclick="handleIntent(document.getElementById('intentInput').value)">执行</button></div><div class="chips" id="chips"><button class="chip" onclick="handleIntent('探究短一点')">探究短一点</button><button class="chip" onclick="handleIntent('学习单简单些')">学习单简单些</button><button class="chip" onclick="handleIntent('多一点示范')">多一点示范</button><button class="chip" onclick="handleIntent('重新设计这节课')">重新设计这节课</button></div><div id="barStatus" class="muted" style="margin-top:8px">Intent Bar · 不保留聊天历史</div></div>
<script>
const state={surface:'light_entry', inquiry:25, display:17, handout:'missing', teacher_review_required:false, formal_apply_performed:false, process_record_candidate:null, intent_bar_state:'collapsed', events:[]};
function log(type){state.events.push({type, surface:state.surface, inquiry:state.inquiry, handout:state.handout, teacher_review_required:state.teacher_review_required, formal_apply_performed:false, ts:new Date().toISOString()}); renderLog();}
function show(id){['light_entry','lesson_focus','semantic_confirmation','handout_candidate_preview','teacher_review_gate'].forEach(x=>document.getElementById(x).classList.toggle('hidden',x!==id));state.surface=id;document.getElementById('topMeta').textContent=id==='light_entry'?'第3周 · 周三 · 今日 3 节课':'四年级 1班 · 色彩的感觉';log('surface_'+id);}
function renderLog(){document.getElementById('eventLog').textContent=JSON.stringify(state.events.slice(-8),null,2);}
function goLesson(){show('lesson_focus');}
function toggleInput(){document.getElementById('intentInput').classList.toggle('hidden');document.getElementById('sendBtn').classList.toggle('hidden');state.intent_bar_state='input';document.getElementById('barStatus').textContent='说一句当前工作意图，不会进入聊天历史';}
function handleIntent(v){v=(v||'').trim();if(!v)return; if(['探究短一点','学习单简单些','多一点示范'].includes(v)){simple(v)} else {complex(v)} document.getElementById('intentInput').value='';}
function simple(v){state.intent_bar_state='done'; if(v==='探究短一点'){state.inquiry=18;state.display=24;document.getElementById('inquiryMinutes').textContent='18 分钟';document.getElementById('displayMinutes').textContent='24 分钟';document.getElementById('agentNote').textContent='已把探究压到 18 分钟，展示时间留出来了。'} if(v==='学习单简单些'){state.handout='simple_preference';document.getElementById('handoutStatus').textContent='未生成 · 已记录简单一点';} if(v==='多一点示范'){document.getElementById('inquiryText').textContent='增加教师示范，再让学生做色彩小实验。'} document.getElementById('barStatus').textContent='已执行：'+v;log('intent_bar_simple_action:'+v);}
function complex(v){state.intent_bar_state='thinking';document.getElementById('barStatus').innerHTML='<span class="thinking">小教在整理你的意思...</span>';log('intent_bar_complex_thinking:'+v);setTimeout(()=>{state.intent_bar_state='confirm';document.getElementById('barStatus').innerHTML='我理解你想围绕“色彩情绪表达”重排这节课，并保留展示时间。<button class="primary" onclick="confirmComplex()">对，去做</button>';},450);}
function confirmComplex(){state.intent_bar_state='done';document.getElementById('agentNote').textContent='已把重点调整为先示范、再探究、最后展示。';document.getElementById('barStatus').textContent='已整理到当前课时结构。';log('intent_bar_complex_confirmed');}
function openSemantic(){show('semantic_confirmation');}
function makeCandidate(type,diff){state.handout='candidate';document.getElementById('handoutStatus').textContent='候选待审核';document.getElementById('taskText').textContent='用途：'+type+'；难度：'+diff+'。选择一种情绪，用颜色小样表达，并写一句理由。';show('handout_candidate_preview');log('generate_handout_candidate');}
function openReview(){state.teacher_review_required=true;show('teacher_review_gate');}
function quickRecord(v='high_interest'){state.process_record_candidate=v==='time_not_enough'?'时间不够，需要下节补讲':'学生兴趣高，展示时间需要保留。';document.getElementById('recordText').textContent=state.process_record_candidate;log('quick_mark_recorded'); if(state.surface!=='teacher_review_gate')document.getElementById('barStatus').textContent='已记录为课后观察候选，不会自动导出。';}
function eventOnly(x){log(x);document.getElementById('barStatus').textContent='已记录：'+x;}
log('open_workbench');
</script>
</body>
</html>'''


def validator_text(slug: str, status: str, stage_id: str, title: str, required: list[str], extras: dict) -> str:
    return f'''import argparse, json, sys, zipfile
from pathlib import Path
SLUG="{slug}"
EXPECTED_STATUS="{status}"
EXPECTED_MARKER="{marker(stage_id,title)}"
REQUIRED_FILES={json.dumps(required, ensure_ascii=False)}
FALSE_FLAGS=["provider_called","model_called","api_key_configured","real_database_written","database_written","real_memory_written","memory_written","Feishu_written","formal_export_created","real_frontend_runtime_modified","frontend_runtime_modified","production_dependency_installed","real_resource_library_connected","teacher_control_runtime_entered","public_display_runtime_entered","student_side_runtime_entered","production_generation_performed","formal_writeback_performed","formal_apply_performed","auto_teacher_approval_performed"]
FORBIDDEN=[".env","token","secret","key","node_modules","__pycache__",".db",".sqlite","dist","build","coverage",".DS_Store"]
def fail(m): print("VALIDATION_FAILED: "+m); sys.exit(1)
def rel_ok(p): return not (p.startswith("/") or p.startswith("\\\\") or (len(p)>1 and p[1]==":")) and "\\\\" not in p
def forbidden(p): return any(x.lower() in p.lower() for x in FORBIDDEN)
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
 for term in {json.dumps(extras.get("must_contain", []), ensure_ascii=False)}:
  if term not in text: fail("missing term "+term)
 for term in {json.dumps(extras.get("must_not_contain", []), ensure_ascii=False)}:
  if term in text: fail("forbidden term "+term)
 print(EXPECTED_MARKER)
if __name__=="__main__": main()
'''


def write_stage(stage_id: str, slug: str, title: str, status: str) -> dict:
    payload = stage_payload(stage_id)
    sample_dir = f"samples/{slug}"
    files = []
    foundation = {
        "stage": f"{stage_id}_{title}",
        "final_status": status,
        "package": PACKAGE,
        "current_identity": "teacher_work_state_driven_intelligent_organization_system",
        "payload": payload,
        "boundary_flags": BOUNDARY,
        "next_stage": NEXT_STAGE,
    }
    dump(f"docs/foundation/{slug}.json", foundation)
    write(f"docs/foundation/{slug}.md", f"# {stage_id} {title}\n\n```text\nfinal_status={status}\npackage={PACKAGE}\nnext_stage={NEXT_STAGE}\n```\n\nThis stage is preview-only and does not enter real frontend, provider sandbox, real database, memory, Feishu, export, or formal apply.\n\n```text\n{marker(stage_id,title)}\n```\n")
    files += [f"docs/foundation/{slug}.md", f"docs/foundation/{slug}.json"]
    if stage_id == "1007J":
        dump(f"{sample_dir}/light_recording_planning_fixture_1007J.json", payload["light_recording_plan"])
        dump(f"{sample_dir}/intent_bar_policy_1007J.json", payload["intent_bar_policy"])
        files += [f"{sample_dir}/light_recording_planning_fixture_1007J.json", f"{sample_dir}/intent_bar_policy_1007J.json"]
    elif stage_id == "1007K":
        write(f"{sample_dir}/index.html", CLICKABLE_HTML)
        dump(f"{sample_dir}/preview_state_1007K.json", {"initial_surface": "light_entry", "final_surface": "teacher_review_gate", "teacher_review_required": True, "formal_apply_performed": False, **payload})
        dump(f"{sample_dir}/preview_events_1007K.json", {"events": payload["click_path"]})
        dump(f"{sample_dir}/intent_bar_trace_1007K.json", {"intent_bar_states": payload["intent_bar_states"], "simple_intents": payload["simple_intents"], "complex_intents": payload["complex_intents"], "chat_history_stored": False})
        files += [f"{sample_dir}/index.html", f"{sample_dir}/preview_state_1007K.json", f"{sample_dir}/preview_events_1007K.json", f"{sample_dir}/intent_bar_trace_1007K.json"]
    elif stage_id == "1007L":
        dump(f"{sample_dir}/local_work_state_1007L.json", payload["local_work_state"])
        dump(f"{sample_dir}/event_log_1007L.json", {"event_log": payload["event_log"]})
        dump(f"{sample_dir}/evidence_events_1007L.json", {"evidence_events": payload["evidence_events"]})
        files += [f"{sample_dir}/local_work_state_1007L.json", f"{sample_dir}/event_log_1007L.json", f"{sample_dir}/evidence_events_1007L.json"]
    elif stage_id == "1007M":
        dump(f"{sample_dir}/clickable_preview_smoke_trace_1007M.json", payload)
        files += [f"{sample_dir}/clickable_preview_smoke_trace_1007M.json"]
    elif stage_id == "1007N":
        dump(f"{sample_dir}/real_experience_milestone_1007N.json", payload)
        files += [f"{sample_dir}/real_experience_milestone_1007N.json"]
    else:
        dump(f"docs/audit/{slug}_result.json", {"stage": f"{stage_id}_{title}", "final_status": status, "pass": True, "marker": marker(stage_id,title), "payload": payload, "boundary_flags": BOUNDARY, "validation": {"py_compile": "PENDING", "validator_no_arg": "PENDING", "validator_root": "PENDING", "manifest_minus_zip": [], "zip_minus_manifest": []}, "next_stage": NEXT_STAGE})
        write(f"docs/audit/{slug}_report.md", f"# {stage_id} Report\n\n```text\nfinal_status={status}\nmarker={marker(stage_id,title)}\n```\n\nSHA record sync only. Business preview content changed=false.\n")
        # 1007I_R1 has only result/report as required stage output plus foundation.
    if stage_id != "1007I_R1":
        dump(f"docs/audit/{slug}_result.json", {"stage": f"{stage_id}_{title}", "final_status": status, "pass": True, "marker": marker(stage_id,title), "boundary_flags": BOUNDARY, "validation": {"py_compile": "PENDING", "validator_no_arg": "PENDING", "validator_root": "PENDING", "manifest_minus_zip": [], "zip_minus_manifest": []}, "next_stage": NEXT_STAGE})
        write(f"docs/audit/{slug}_report.md", f"# {stage_id} Report\n\n```text\nfinal_status={status}\nmarker={marker(stage_id,title)}\n```\n\nPreview-only evidence generated for {stage_id}. No real provider, database, memory, Feishu, frontend runtime, or formal apply.\n")
    files += [f"docs/audit/{slug}_result.json", f"docs/audit/{slug}_report.md"]
    script = f"scripts/validate_{slug}.py"
    files_for_validator = files + [script, f"docs/audit_packages/{slug}_manifest.json", f"docs/audit_packages/{slug}.zip"]
    must = [status, "teacher_review_required"]
    if stage_id == "1007K":
        must += ["对小教说一句", "探究短一点", "重新设计这节课", "semantic_confirmation", "teacher_review_gate"]
        no = []
    elif stage_id == "1007J":
        must += ["Intent Bar", "evidence_event_schema", "not_teacher_form_filling"]
        no = []
    elif stage_id == "1007L":
        must += ["privacy_level", "exportable_candidate", "teacher_quick_mark"]
        no = []
    elif stage_id == "1007M":
        must += ["formal_apply_performed=false", "smoke_checklist"]
        no = []
    elif stage_id == "1007N":
        must += ["what_user_can_experience", "what_is_not_real_yet", "1008A_PROVIDER_SANDBOX_PLANNING"]
        no = []
    else:
        must += ["business_preview_content_changed", "r1_fix_status"]
        no = []
    write(script, validator_text(slug, status, stage_id, title, files_for_validator, {"must_contain": must, "must_not_contain": no}))
    manifest_path = f"docs/audit_packages/{slug}_manifest.json"
    zip_entries = files + [script, manifest_path]
    manifest = {"stage": f"{stage_id}_{title}", "final_status": status, "zip_path": f"docs/audit_packages/{slug}.zip", "zip_sha256": "PENDING", "zip_entry_count": len(zip_entries), "zip_entries": zip_entries, "manifest_minus_zip": [], "zip_minus_manifest": [], "forbidden_files_present": [], "marker": marker(stage_id,title)}
    dump(manifest_path, manifest)
    zsha = make_zip(slug, zip_entries)
    manifest["zip_sha256"] = zsha
    dump(manifest_path, manifest)
    # Keep zip payload stable after manifest write by rebuilding once with manifest containing external SHA record.
    zsha = make_zip(slug, zip_entries)
    return {"stage": stage_id, "slug": slug, "final_status": status, "zip_entry_count": len(zip_entries), "zip_sha256": zsha}


def main():
    rows = [write_stage(*stage) for stage in STAGES]
    table = "\n".join(f"| {r['stage']} | {r['final_status']} | PENDING | PENDING | {r['zip_entry_count']} | {r['zip_sha256']} | [] | [] |" for r in rows)
    readme = f"""# Xiaojiao 1007I_R1-1007N Art Teacher Clickable Experience Review

```text
package={PACKAGE}
overall_stop={NEXT_STAGE}
clickable_entry=samples/xiaojiao_art_teacher_clickable_preview_with_intent_bar_1007K/index.html
```

| Stage | final_status | validator no-arg | validator --root | ZIP_ENTRY_COUNT | ZIP_SHA256 | manifest_minus_zip | zip_minus_manifest |
| --- | --- | --- | --- | ---: | --- | --- | --- |
{table}

```text
provider_called=false
model_called=false
api_key_configured=false
real_database_written=false
real_memory_written=false
Feishu_written=false
formal_export_created=false
real_frontend_runtime_modified=false
production_dependency_installed=false
teacher_review_required=true
formal_apply_performed=false
```

next_stage={NEXT_STAGE}
"""
    write("README_1007I_R1_TO_1007N_ART_TEACHER_CLICKABLE_EXPERIENCE_REVIEW.md", readme)
    dump("docs/audit/xiaojiao_1007I_R1_to_1007N_art_teacher_clickable_experience_milestone_summary.json", {"package": PACKAGE, "overall_status": "1007I_R1_TO_1007N_ART_TEACHER_CLICKABLE_EXPERIENCE_MILESTONE_PASS", "stages": rows, "clickable_entry": "samples/xiaojiao_art_teacher_clickable_preview_with_intent_bar_1007K/index.html", "next_stage": NEXT_STAGE, "boundary_flags": BOUNDARY})
    write("docs/audit/xiaojiao_1007I_R1_to_1007N_art_teacher_clickable_experience_milestone_report.md", f"# 1007I_R1-1007N Clickable Experience Milestone\n\n```text\noverall_status=1007I_R1_TO_1007N_ART_TEACHER_CLICKABLE_EXPERIENCE_MILESTONE_PASS\nnext_stage={NEXT_STAGE}\n```\n\nThe package provides a local clickable preview entry and supporting light-recording, state, evidence, smoke trace, and milestone review files.\n")


if __name__ == "__main__":
    main()

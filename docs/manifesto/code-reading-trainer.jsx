import { useState } from "react";

const STEPS = [
  {
    id: "intro",
    phase: "Welcome",
    title: "How to Read This Repo Without Getting Lost",
    subtitle: "A practical method for non-coders",
    description: "You do not need to read everything. You need a map.\n\nIn this repo, the map is always: SHAPES -> FILE MAP -> ORCHESTRATOR -> ONE DECISION FILE -> ADAPTER CONTRACT.\n\nWhen you follow that order, abstract code becomes concrete.",
    visual: "overview",
  },
  {
    id: "shapes-intro",
    phase: "Step 1",
    title: "Read the Data Shapes First",
    subtitle: "Understand WHAT the tool manipulates",
    description: "In `label_generator`, the domain models are in `core/label_generator/domain/models.py`.\n\nRead class names first. They are the nouns:\n• `LabelFieldConfig`\n• `LabelJob`\n• `PreparedField`\n• `LabelSlot`\n• `RenderPlan`\n\nYou can understand the program story before reading any algorithm.",
    visual: "shapes-overview",
  },
  {
    id: "shape-1",
    phase: "Step 1",
    title: "LabelJob — The core input shape",
    subtitle: "Everything needed for one run",
    description: "`LabelJob` is the normalized input the decision layer consumes. It combines sheet name, rows, field config, copies, and options.\n\nThis tells you exactly what the decision engine needs, independent of Flask, files, or PDF libraries.",
    visual: "shape-rawrecord",
    code: {
      lines: [
        { text: "@dataclass", highlight: false, note: "" },
        { text: "class LabelJob:", highlight: true, note: "Normalized decision input" },
        { text: "    sheet_name: str", highlight: false, note: "Selected worksheet name" },
        { text: "    rows: list[dict[str, Any]]", highlight: true, note: "Data rows from worksheet" },
        { text: "    fields: list[LabelFieldConfig]", highlight: true, note: "What text to place on labels" },
        { text: "    copies_per_record: int", highlight: false, note: "" },
        { text: "    use_template: bool", highlight: false, note: "" },
      ],
    },
  },
  {
    id: "shape-2",
    phase: "Step 1",
    title: "RenderPlan — The core output shape",
    subtitle: "A complete print plan, not a PDF",
    description: "`RenderPlan` is the decision result: counts and slot placements. It is pure data.\n\nImportant mindset: core does NOT create PDF bytes. Core creates a plan. Adapter `io.py` renders that plan.",
    visual: "shape-label",
    code: {
      lines: [
        { text: "@dataclass", highlight: false, note: "" },
        { text: "class RenderPlan:", highlight: true, note: "Decision output shape" },
        { text: "    input_rows: int", highlight: false, note: "" },
        { text: "    filtered_rows: int", highlight: false, note: "" },
        { text: "    total_labels: int", highlight: true, note: "How many labels will render" },
        { text: "    labels_per_page: int", highlight: false, note: "" },
        { text: "    slots: list[LabelSlot]", highlight: true, note: "Exact placement instructions" },
      ],
    },
  },
  {
    id: "shape-3",
    phase: "Step 1",
    title: "LabelSlot + PreparedField — The placement details",
    subtitle: "Exactly what gets drawn and where",
    description: "`LabelSlot` says where on the page. `PreparedField` says what text/style to draw in that slot.\n\nTogether they connect business decisions to rendering, without coupling to any PDF library.",
    visual: "shape-position",
    code: {
      lines: [
        { text: "@dataclass", highlight: false, note: "" },
        { text: "class LabelSlot:", highlight: true, note: "One physical slot on a page" },
        { text: "    page_index: int", highlight: false, note: "" },
        { text: "    slot_index: int", highlight: false, note: "" },
        { text: "    x_in: float", highlight: true, note: "Position in inches" },
        { text: "    y_in: float", highlight: true, note: "Position in inches" },
        { text: "    fields: list[PreparedField]", highlight: true, note: "Text/style entries for that slot" },
      ],
    },
  },
  {
    id: "shapes-flow",
    phase: "Step 1",
    title: "The Data Flow",
    subtitle: "Now you can see the whole journey",
    description: "From shapes only, you already have the story:\n\n• Adapter reads worksheet rows\n• Core normalizes into `LabelJob`\n• Core computes `RenderPlan` with `LabelSlot`s\n• Adapter renders PDF from that plan\n\nThis is why shape-first reading works.",
    visual: "flow",
  },
  {
    id: "file-map",
    phase: "Step 2",
    title: "Read FILE_MAP Before Functions",
    subtitle: "See responsibility split at a glance",
    description: "Open `core/<tool>/application/FILE_MAP.md`.\n\nIt tells you which file owns what responsibility. This is your anti-overwhelm tool.\n\nFor `label_generator`:\n• `input_validation.py` -> build/validate job\n• `planning.py` -> compute slots/plan\n• `output_format.py` -> serialize result\n• `service.py` -> facade/re-exports\n• `orchestrator.py` -> dumb sequence",
    visual: "orchestrator",
    code: {
      lines: [
        { text: "- input_validation.py -> build_job()", highlight: true, note: "normalize + validate" },
        { text: "- planning.py -> compute_plan()", highlight: true, note: "placement decisions" },
        { text: "- output_format.py -> to_result_dict()", highlight: true, note: "response shaping" },
        { text: "- service.py -> facade only", highlight: false, note: "compat layer" },
        { text: "- orchestrator.py -> run()", highlight: true, note: "3-line sequence" },
      ],
    },
  },
  {
    id: "orch-intro",
    phase: "Step 3",
    title: "Read the Orchestrator Second",
    subtitle: "The table of contents for your program",
    description: "Your orchestrator should be tiny and branchless. In this repo it is intentionally dumb.\n\nRead it as plot only: validate/build input -> compute decisions -> format output.",
    visual: "orchestrator",
  },
  {
    id: "orch-code",
    phase: "Step 3",
    title: "Reading the Orchestrator Line by Line",
    subtitle: "Every line is one step in the recipe",
    description: "This is the real shape of our orchestrator style. No branching. No loops. No side effects.\n\nIf the orchestrator gets complicated, logic belongs in a decision module instead.",
    visual: "orch-annotated",
    code: {
      lines: [
        { text: "def run(payload: dict[str, Any]) -> dict[str, Any]:", highlight: false, note: "Entrypoint" },
        { text: "", highlight: false, note: "" },
        { text: "    job = service.build_job(payload)", highlight: true, note: "🧠 validate/normalize data" },
        { text: "    plan = service.compute_plan(job)", highlight: true, note: "🧠 decision computation" },
        { text: "    return service.to_result_dict(job, plan)", highlight: true, note: "🧠 pure output mapping" },
      ],
    },
  },
  {
    id: "sandwich",
    phase: "Step 3",
    title: "See the Sandwich Pattern",
    subtitle: "Plumbing → Decisions → Plumbing",
    description: "In this repo, the adapter handles plumbing, core handles decisions.\n\nAdapter (`app.py`/`presenter.py`/`io.py`) -> Core (`build_job`, `compute_plan`) -> Adapter render/response.\n\nThis keeps core reusable for any future UI framework.",
    visual: "sandwich",
  },
  {
    id: "func-intro",
    phase: "Step 4",
    title: "Read Functions Only When You Need To",
    subtitle: "Zoom in on one piece at a time",
    description: "Use a question-driven zoom:\n\n\"Why did payload fail?\" -> `input_validation.py`\n\"Why are positions weird?\" -> `planning.py`\n\"Why is response shape wrong?\" -> `output_format.py`\n\"Why UI not matching request?\" -> adapter `presenter.py` + `UI_CONTRACT.md`\n\nRead only one module at a time.",
    visual: "zoom",
  },
  {
    id: "func-example",
    phase: "Step 4",
    title: "Reading One Decision Function",
    subtitle: "_resolve_text — from row + field config to printable text",
    description: "This function is pure decision logic. No files, no HTTP, no PDF library.\n\nIt explains how static fields vs worksheet fields become final text, and how header formatting is applied.",
    visual: "func-detail",
    code: {
      lines: [
        { text: "def _resolve_text(row, field) -> str:", highlight: true, note: "Pure transformation" },
        { text: "    if field.is_static:", highlight: false, note: "" },
        { text: "        raw_text = field.static_text", highlight: true, note: "Static mode" },
        { text: "    else:", highlight: false, note: "" },
        { text: '        value = row.get(field.column or "", "")', highlight: false, note: "Worksheet mode" },
        { text: "        raw_text = \"\" if value is None else str(value)", highlight: false, note: "" },
        { text: "        if raw_text.strip().lower() == \"nan\":", highlight: false, note: "Normalize blanks" },
        { text: "            raw_text = \"\"", highlight: false, note: "" },
        { text: "        if raw_text.strip():", highlight: false, note: "" },
        { text: "            raw_text = f\"{field.prefix}{raw_text}{field.suffix}\"", highlight: false, note: "" },
        { text: "", highlight: false, note: "" },
        { text: "    text = raw_text.strip()", highlight: false, note: "" },
        { text: "    return text.upper() if field.is_header else text", highlight: true, note: "Header decision" },
      ],
    },
  },
  {
    id: "verify",
    phase: "Step 5",
    title: "Verify with Your Eyes",
    subtitle: "Use artifacts, not guesswork",
    description: "Verification here means checking the right artifact at each layer:\n\n• `examples/*.json` -> do payloads match expectations?\n• `contracts.run(...)` result -> is core output shape right?\n• `UI_CONTRACT.md` -> does adapter route/state behavior match docs?\n• PDF output -> final visual check.\n\nYou can still use print/debug, but artifacts are your ground truth.",
    visual: "verify",
  },
  {
    id: "verify-how",
    phase: "Step 5",
    title: "Visual Verification in Practice",
    subtitle: "A concrete inspection sequence",
    description: "When behavior looks wrong, inspect in this exact order:\n\n1) Input payload from UI\n2) `build_generate_payload` output in presenter\n3) `contracts.run` result\n4) adapter rendering step\n\nThis sequence isolates whether the bug is mapping, decision, or rendering.",
    visual: "verify-code",
    code: {
      lines: [
        { text: "# 1) Adapter request mapping", highlight: false, note: "" },
        { text: "payload = presenter.build_generate_payload(body, rows)", highlight: true, note: "Check mapped payload" },
        { text: "print(payload.keys())", highlight: true, note: "sheet_name, rows, label_config..." },
        { text: "", highlight: false, note: "" },
        { text: "# 2) Core contract", highlight: false, note: "" },
        { text: "result = run_contract(ToolInput(payload=payload)).result", highlight: true, note: "Pure decision output" },
        { text: "print(result['total_labels'])", highlight: true, note: "Count sanity check" },
        { text: "", highlight: false, note: "" },
        { text: "# 3) Adapter rendering", highlight: false, note: "" },
        { text: "io.render_plan_to_pdf(result, output_path)", highlight: true, note: "Rendering boundary" },
        { text: "return io.pdf_response(output_path, result['download_name'])", highlight: true, note: "Final response" },
      ],
    },
  },
  {
    id: "mental-model",
    phase: "Summary",
    title: "Your New Reading Method",
    subtitle: "Use this every time you open a tool",
    description: "1. SHAPES: `domain/models.py`\n2. FILE SPLIT: `application/FILE_MAP.md`\n3. ORCHESTRATOR: `application/orchestrator.py`\n4. ZOOM: one responsibility file at a time\n5. VERIFY: examples -> contract output -> UI contract -> final UI/PDF\n\nYou don't need to hold everything in your head. The architecture is now designed to externalize the map.",
    visual: "summary",
  },
];

const PHASES = ["Welcome", "Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Summary"];
const PHASE_LABELS = {
  "Welcome": "Start",
  "Step 1": "Data Shapes",
  "Step 2": "File Map",
  "Step 3": "Orchestrator",
  "Step 4": "Functions",
  "Step 5": "Verify",
  "Summary": "Method",
};

function CodeViewer({ code }) {
  if (!code) return null;
  return (
    <div style={{
      background: "#1a1a2e",
      borderRadius: 12,
      padding: "20px 24px",
      fontFamily: "'JetBrains Mono', 'Fira Code', 'SF Mono', monospace",
      fontSize: 13,
      lineHeight: 1.8,
      overflowX: "auto",
      marginTop: 16,
    }}>
      {code.lines.map((line, i) => (
        <div key={i} style={{
          display: "flex",
          gap: 16,
          alignItems: "baseline",
          padding: "2px 0",
          background: line.highlight ? "rgba(99, 179, 237, 0.1)" : "transparent",
          borderLeft: line.highlight ? "3px solid #63b3ed" : "3px solid transparent",
          paddingLeft: 12,
          marginLeft: -12,
          borderRadius: 2,
        }}>
          <span style={{
            color: line.highlight ? "#e2e8f0" : "#718096",
            whiteSpace: "pre",
            minWidth: 0,
            flexShrink: 0,
          }}>
            {line.text || " "}
          </span>
          {line.note && (
            <span style={{
              color: "#63b3ed",
              fontSize: 12,
              whiteSpace: "nowrap",
              opacity: 0.9,
              flexShrink: 0,
            }}>
              {line.note}
            </span>
          )}
        </div>
      ))}
    </div>
  );
}

function DataFlowVisual() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, padding: "20px 0" }}>
      {[
        { shape: "LabelJob", desc: "Normalized core input", color: "#ed8936", icon: "📋" },
        { shape: null, desc: "compute_plan()", color: null, arrow: true },
        { shape: "RenderPlan", desc: "Pure placement output", color: "#48bb78", icon: "🧠" },
        { shape: null, desc: "to_result_dict()", color: null, arrow: true },
        { shape: "Contract Result", desc: "Adapter-ready shape", color: "#63b3ed", icon: "🔌" },
        { shape: null, desc: "render_plan_to_pdf()", color: null, arrow: true },
        { shape: "PDF File", desc: "Final printed output", color: "#b794f4", icon: "📄" },
      ].map((item, i) => item.arrow ? (
        <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2 }}>
          <div style={{ width: 2, height: 16, background: "#4a5568" }} />
          <div style={{
            background: "#2d3748",
            padding: "4px 16px",
            borderRadius: 20,
            fontSize: 12,
            color: "#a0aec0",
            fontFamily: "'JetBrains Mono', monospace",
          }}>
            {item.desc}
          </div>
          <div style={{ width: 0, height: 0, borderLeft: "6px solid transparent", borderRight: "6px solid transparent", borderTop: "8px solid #4a5568" }} />
        </div>
      ) : (
        <div key={i} style={{
          background: `${item.color}18`,
          border: `2px solid ${item.color}`,
          borderRadius: 12,
          padding: "12px 32px",
          textAlign: "center",
          minWidth: 240,
        }}>
          <div style={{ fontSize: 20, marginBottom: 4 }}>{item.icon}</div>
          <div style={{ fontWeight: 700, fontSize: 16, color: item.color }}>{item.shape}</div>
          <div style={{ fontSize: 12, color: "#a0aec0", marginTop: 2 }}>{item.desc}</div>
        </div>
      ))}
    </div>
  );
}

function SandwichVisual() {
  const layers = [
    { label: "Flask presenter/io", type: "plumbing", icon: "📥" },
    { label: "build_job()", type: "decision", icon: "🧠" },
    { label: "compute_plan()", type: "decision", icon: "🧠" },
    { label: "to_result_dict()", type: "decision", icon: "🧠" },
    { label: "Flask PDF response", type: "plumbing", icon: "📤" },
  ];
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6, padding: "20px 0", maxWidth: 420, margin: "0 auto" }}>
      {layers.map((layer, i) => (
        <div key={i} style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "14px 20px",
          borderRadius: 10,
          background: layer.type === "plumbing" ? "rgba(237, 137, 54, 0.12)" : "rgba(72, 187, 120, 0.12)",
          border: `1.5px solid ${layer.type === "plumbing" ? "#ed8936" : "#48bb78"}`,
        }}>
          <span style={{ fontSize: 22 }}>{layer.icon}</span>
          <div>
            <div style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 14,
              color: layer.type === "plumbing" ? "#ed8936" : "#48bb78",
              fontWeight: 600,
            }}>
              {layer.label}
            </div>
            <div style={{
              fontSize: 11,
              color: "#718096",
              textTransform: "uppercase",
              letterSpacing: 1,
              marginTop: 2,
            }}>
              {layer.type}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function ShapeVisual({ type }) {
  if (type === "shape-rawrecord") {
    return (
      <div style={{ padding: "16px 0" }}>
        <div style={{
          background: "rgba(237, 137, 54, 0.08)",
          border: "2px solid #ed8936",
          borderRadius: 12,
          padding: 20,
          maxWidth: 380,
          margin: "0 auto",
        }}>
          <div style={{ fontSize: 12, color: "#ed8936", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
            LabelJob — normalized run input
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <tbody>
              {[["sheet_name", "Stars Collide"], ["rows", "[{...}, {...}]"], ["fields", "[LabelFieldConfig, ...]"], ["copies_per_record", "1"], ["use_template", "true"]].map(([k, v], i) => (
                <tr key={i}>
                  <td style={{ padding: "4px 8px", fontSize: 13, color: "#a0aec0", fontFamily: "monospace", borderBottom: "1px solid #2d3748" }}>{k}</td>
                  <td style={{ padding: "4px 8px", fontSize: 13, color: "#e2e8f0", fontFamily: "monospace", borderBottom: "1px solid #2d3748" }}>{v}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
  if (type === "shape-label") {
    return (
      <div style={{ padding: "16px 0", display: "flex", justifyContent: "center" }}>
        <div style={{
          background: "rgba(72, 187, 120, 0.08)",
          border: "2px solid #48bb78",
          borderRadius: 12,
          padding: 20,
          width: 240,
          textAlign: "center",
        }}>
          <div style={{ fontSize: 12, color: "#48bb78", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
            RenderPlan — core output
          </div>
          <div style={{
            background: "white",
            border: "1px solid #e2e8f0",
            borderRadius: 6,
            padding: "12px 16px",
            textAlign: "left",
            fontFamily: "monospace",
            fontSize: 13,
            lineHeight: 1.6,
            color: "#1a202c",
          }}>
              <div>input_rows: 22</div>
              <div>total_labels: 22</div>
              <div>slots: [...LabelSlot]</div>
            </div>
          </div>
      </div>
    );
  }
  if (type === "shape-position") {
    return (
      <div style={{ padding: "16px 0", display: "flex", justifyContent: "center" }}>
        <div style={{
          background: "rgba(99, 179, 237, 0.08)",
          border: "2px solid #63b3ed",
          borderRadius: 12,
          padding: 20,
          position: "relative",
        }}>
          <div style={{ fontSize: 12, color: "#63b3ed", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
            LabelSlot — placed on page
          </div>
          <div style={{
            background: "#f7fafc",
            border: "1px solid #cbd5e0",
            borderRadius: 4,
            width: 200,
            height: 260,
            position: "relative",
            margin: "0 auto",
          }}>
            <div style={{
              position: "absolute",
              top: 16,
              left: 12,
              width: 56,
              height: 24,
              background: "rgba(99, 179, 237, 0.2)",
              border: "2px solid #63b3ed",
              borderRadius: 3,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 7,
              color: "#2b6cb0",
              fontFamily: "monospace",
            }}>
              GD-DH1
            </div>
            {[1,2,3,4,5,6,7,8].map(i => (
              <div key={i} style={{
                position: "absolute",
                top: 16 + Math.floor(i / 3) * 28,
                left: 12 + (i % 3) * 62,
                width: 56,
                height: 24,
                background: "#edf2f7",
                border: "1px solid #e2e8f0",
                borderRadius: 3,
              }} />
            ))}
            <div style={{
              position: "absolute",
              top: 4,
              left: 4,
              fontSize: 8,
              color: "#a0aec0",
            }}>
              page 0
            </div>
          </div>
        </div>
      </div>
    );
  }
  return null;
}

function VerifyVisual() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, padding: "16px 0" }}>
      {[
        { step: "Presenter payload", output: '{"sheet_name": "...", "rows": [...], "label_config": {...}}', emoji: "🔄", color: "#ed8936" },
        { step: "Contract result", output: '{"total_labels": 22, "slots": [...], "download_name": "..."}', emoji: "🧠", color: "#48bb78" },
        { step: "UI contract check", output: "POST /generate -> PDF\nErrors return {error: string}", emoji: "📘", color: "#63b3ed" },
        { step: "Visual output", output: "Open generated PDF and verify alignment/text", emoji: "👁", color: "#b794f4" },
      ].map((item, i) => (
        <div key={i} style={{
          display: "flex",
          gap: 12,
          alignItems: "flex-start",
          padding: "12px 16px",
          background: `${item.color}10`,
          borderRadius: 10,
          borderLeft: `3px solid ${item.color}`,
        }}>
          <span style={{ fontSize: 24, flexShrink: 0, lineHeight: 1 }}>{item.emoji}</span>
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: item.color, marginBottom: 4 }}>{item.step}</div>
            <pre style={{
              margin: 0,
              fontSize: 12,
              color: "#a0aec0",
              fontFamily: "'JetBrains Mono', monospace",
              whiteSpace: "pre-wrap",
            }}>
              {item.output}
            </pre>
          </div>
        </div>
      ))}
    </div>
  );
}

function SummaryVisual() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16, padding: "16px 0" }}>
      {[
        { num: "1", title: "SHAPES", desc: "Read dataclasses. Learn the nouns.", color: "#ed8936", time: "2 minutes" },
        { num: "2", title: "ORCHESTRATOR", desc: "Read the main function. Learn the plot.", color: "#48bb78", time: "2 minutes" },
        { num: "3", title: "ZOOM IN", desc: "Read one function when you have a question.", color: "#63b3ed", time: "As needed" },
        { num: "4", title: "VERIFY VISUALLY", desc: "Print intermediate data. Look with your eyes.", color: "#b794f4", time: "5 minutes" },
      ].map((item, i) => (
        <div key={i} style={{
          display: "flex",
          gap: 16,
          alignItems: "center",
          padding: "16px 20px",
          background: `${item.color}10`,
          border: `2px solid ${item.color}40`,
          borderRadius: 14,
        }}>
          <div style={{
            width: 44,
            height: 44,
            borderRadius: "50%",
            background: item.color,
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            fontSize: 20,
            flexShrink: 0,
          }}>
            {item.num}
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 800, fontSize: 16, color: item.color, letterSpacing: 1 }}>{item.title}</div>
            <div style={{ fontSize: 14, color: "#a0aec0", marginTop: 2 }}>{item.desc}</div>
          </div>
          <div style={{
            fontSize: 11,
            color: "#718096",
            background: "#2d3748",
            padding: "4px 10px",
            borderRadius: 20,
            flexShrink: 0,
          }}>
            {item.time}
          </div>
        </div>
      ))}
    </div>
  );
}

function VisualPanel({ step }) {
  switch (step.visual) {
    case "overview":
      return (
        <div style={{ textAlign: "center", padding: "40px 20px" }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>🏗️</div>
          <div style={{ fontSize: 14, color: "#718096", maxWidth: 280, margin: "0 auto", lineHeight: 1.6 }}>
            A building makes sense from the floor plan.<br />Code makes sense from the data shapes.
          </div>
        </div>
      );
    case "shapes-overview":
      return (
        <div style={{ textAlign: "center", padding: "30px 20px" }}>
          <div style={{ display: "flex", justifyContent: "center", gap: 16, flexWrap: "wrap" }}>
            {[
              { name: "LabelFieldConfig", icon: "⚙️", color: "#ed8936" },
              { name: "LabelJob", icon: "📋", color: "#48bb78" },
              { name: "LabelSlot", icon: "📐", color: "#63b3ed" },
              { name: "RenderPlan", icon: "🧠", color: "#b794f4" },
            ].map((s, i) => (
              <div key={i} style={{
                background: `${s.color}15`,
                border: `2px solid ${s.color}`,
                borderRadius: 12,
                padding: "16px 20px",
                textAlign: "center",
                width: 120,
              }}>
                <div style={{ fontSize: 28, marginBottom: 6 }}>{s.icon}</div>
                <div style={{ fontSize: 13, fontWeight: 700, color: s.color }}>{s.name}</div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: 16, fontSize: 13, color: "#718096" }}>
            These are the nouns of your program
          </div>
        </div>
      );
    case "shape-rawrecord":
    case "shape-label":
    case "shape-position":
      return <ShapeVisual type={step.visual} />;
    case "flow":
      return <DataFlowVisual />;
    case "orchestrator":
      return (
        <div style={{ textAlign: "center", padding: "30px 20px" }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>📖</div>
          <div style={{ fontSize: 14, color: "#718096", maxWidth: 300, margin: "0 auto", lineHeight: 1.6 }}>
            The orchestrator is a tiny recipe.<br />Flow lives here.<br />Details live in split modules.
          </div>
        </div>
      );
    case "sandwich":
      return <SandwichVisual />;
    case "zoom":
      return (
        <div style={{ textAlign: "center", padding: "30px 20px" }}>
          <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 16 }}>
            <span style={{ fontSize: 32, opacity: 0.3 }}>🔍</span>
            <span style={{ fontSize: 48 }}>🔍</span>
            <span style={{ fontSize: 32, opacity: 0.3 }}>🔍</span>
          </div>
          <div style={{ fontSize: 14, color: "#718096", maxWidth: 300, margin: "0 auto", lineHeight: 1.6 }}>
            Don't read everything.<br />Zoom into the one function<br />that answers your specific question.
          </div>
        </div>
      );
    case "verify":
      return <VerifyVisual />;
    case "summary":
      return <SummaryVisual />;
    default:
      return null;
  }
}

export default function CodeReadingTrainer() {
  const [currentStep, setCurrentStep] = useState(0);
  const step = STEPS[currentStep];
  const progress = ((currentStep) / (STEPS.length - 1)) * 100;

  const currentPhaseIndex = PHASES.indexOf(step.phase);

  return (
    <div style={{
      background: "#0f1119",
      color: "#e2e8f0",
      minHeight: "100vh",
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Progress bar */}
      <div style={{ height: 3, background: "#1a1a2e" }}>
        <div style={{
          height: "100%",
          width: `${progress}%`,
          background: "linear-gradient(90deg, #ed8936, #48bb78, #63b3ed, #b794f4)",
          transition: "width 0.4s ease",
        }} />
      </div>

      {/* Phase indicators */}
      <div style={{
        display: "flex",
        justifyContent: "center",
        gap: 6,
        padding: "16px 20px 8px",
        flexWrap: "wrap",
      }}>
        {PHASES.map((phase, i) => (
          <div
            key={phase}
            style={{
              padding: "5px 14px",
              borderRadius: 20,
              fontSize: 12,
              fontWeight: i === currentPhaseIndex ? 700 : 500,
              background: i === currentPhaseIndex ? "#2d3748" : "transparent",
              color: i === currentPhaseIndex ? "#e2e8f0" : "#4a5568",
              transition: "all 0.3s ease",
              cursor: "pointer",
            }}
            onClick={() => {
              const targetStep = STEPS.findIndex(s => s.phase === phase);
              if (targetStep >= 0) setCurrentStep(targetStep);
            }}
          >
            {PHASE_LABELS[phase]}
          </div>
        ))}
      </div>

      {/* Main content */}
      <div style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        padding: "16px 24px 24px",
        maxWidth: 700,
        margin: "0 auto",
        width: "100%",
        boxSizing: "border-box",
      }}>
        {/* Step label */}
        <div style={{
          fontSize: 12,
          fontWeight: 700,
          color: "#63b3ed",
          textTransform: "uppercase",
          letterSpacing: 2,
          marginBottom: 8,
        }}>
          {step.phase === "Welcome" || step.phase === "Summary" ? step.phase : `${step.phase} of 5`}
          <span style={{ color: "#4a5568", marginLeft: 8 }}>
            {currentStep + 1} / {STEPS.length}
          </span>
        </div>

        {/* Title */}
        <h1 style={{
          fontSize: 26,
          fontWeight: 800,
          color: "#f7fafc",
          margin: "0 0 4px 0",
          lineHeight: 1.2,
        }}>
          {step.title}
        </h1>

        {/* Subtitle */}
        <div style={{
          fontSize: 15,
          color: "#718096",
          marginBottom: 20,
        }}>
          {step.subtitle}
        </div>

        {/* Visual area */}
        <div style={{
          background: "#161822",
          borderRadius: 16,
          padding: "4px 16px",
          marginBottom: 16,
          border: "1px solid #1e2030",
          minHeight: 100,
        }}>
          {step.visual && !step.visual.includes("annotated") && !step.visual.includes("detail") && !step.visual.includes("verify-code") && (
            <VisualPanel step={step} />
          )}
          {step.code && <CodeViewer code={step.code} />}
          {step.visual === "orch-annotated" && !step.code && <VisualPanel step={step} />}
          {step.visual === "verify-code" && !step.code && <VisualPanel step={step} />}
        </div>

        {/* Description */}
        <div style={{
          fontSize: 15,
          lineHeight: 1.75,
          color: "#a0aec0",
          whiteSpace: "pre-line",
          flex: 1,
        }}>
          {step.description}
        </div>

        {/* Navigation */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginTop: 24,
          paddingTop: 16,
          borderTop: "1px solid #1e2030",
        }}>
          <button
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
            style={{
              padding: "10px 24px",
              borderRadius: 10,
              border: "1px solid #2d3748",
              background: "transparent",
              color: currentStep === 0 ? "#2d3748" : "#a0aec0",
              cursor: currentStep === 0 ? "default" : "pointer",
              fontSize: 14,
              fontWeight: 600,
              transition: "all 0.2s",
            }}
          >
            ← Back
          </button>

          <div style={{ display: "flex", gap: 4 }}>
            {STEPS.map((_, i) => (
              <div
                key={i}
                onClick={() => setCurrentStep(i)}
                style={{
                  width: i === currentStep ? 20 : 6,
                  height: 6,
                  borderRadius: 3,
                  background: i === currentStep ? "#63b3ed" : i < currentStep ? "#48bb78" : "#2d3748",
                  cursor: "pointer",
                  transition: "all 0.3s ease",
                }}
              />
            ))}
          </div>

          <button
            onClick={() => setCurrentStep(Math.min(STEPS.length - 1, currentStep + 1))}
            disabled={currentStep === STEPS.length - 1}
            style={{
              padding: "10px 24px",
              borderRadius: 10,
              border: "none",
              background: currentStep === STEPS.length - 1 ? "#2d3748" : "linear-gradient(135deg, #63b3ed, #4299e1)",
              color: currentStep === STEPS.length - 1 ? "#4a5568" : "white",
              cursor: currentStep === STEPS.length - 1 ? "default" : "pointer",
              fontSize: 14,
              fontWeight: 600,
              transition: "all 0.2s",
            }}
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}

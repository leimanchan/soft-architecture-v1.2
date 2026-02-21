# Building Software
# That Stays Soft
A Practical Guide to Decoupled Architecture
for the Age of AI-Assisted Development
No frameworks. No ceremony. Just the discipline that makes code changeable.
Contents
## Part One: The Problem Nobody Talks About
## Chapter 1: Why LLM Code Turns to Concrete
## Chapter 2: The Two Kinds of Code
## Part Two: The Mental Model
## Chapter 3: Decisions vs. Plumbing — The Only Rule You Need
## Chapter 4: A Real Example: The Avery Label Program
## Part Three: The Five Practices
## Chapter 5: Files Are Your Architecture
## Chapter 6: Plain Data at Every Boundary
## Chapter 7: Tests Are Your First Interface
## Chapter 8: The Dumb Orchestrator
## Chapter 9: Side Effects at the Edges
## Part Four: Integration Without Pain
## Chapter 10: Why Integration Breaks Things
## Chapter 11: The Adapter Pattern (Without the Ceremony)
## Chapter 12: Growing a System File by File
## Part Five: Working With LLMs Effectively
## Chapter 13: Prompt Patterns That Enforce Structure
## Chapter 14: The Iterative Build Cycle
## Chapter 15: When to Refactor and When to Rewrite
## Appendix: The Checklist
# Part One
The Problem Nobody Talks About
## Chapter 1: Why LLM Code Turns to Concrete
There is a specific failure mode that happens when you build software with large language models, and it is different from the failure modes of human-written code. Understanding it is the first step to avoiding it.
When you ask an LLM to build something, it optimizes for one thing above all else: making the code work right now. This is not a flaw. It is exactly what you asked for. The problem is that "working right now" and "changeable later" are often in direct tension, and the LLM will always choose the former unless you explicitly guide it otherwise.
Here is what happens in practice. You ask for a program that reads a CSV, processes the data, and outputs a PDF. The LLM produces a single function — maybe 80 lines long — that opens the file, parses the rows, applies your logic, and writes the output. It works. You are pleased.
Then you ask for a change. "Can it also handle Excel files?" The LLM modifies the function, adding a conditional branch at the top. Now the function is 110 lines. It still works.
"Can we sort the data differently depending on a flag?" Another branch. 140 lines. Still works.
"Can it output to a different label format?" More conditionals woven into the output section. 180 lines. Still works, but something has changed. Each new request takes longer. The LLM sometimes breaks a previous feature when adding a new one. You start seeing responses like "I've reorganized the function to accommodate the new requirement" — which means it rewrote large chunks of existing code to wedge in the new behavior.
This is the concrete setting. Your code went from soft and moldable to rigid and brittle in the space of four or five iterations. Not because anyone did anything wrong in any individual step, but because the overall structure was never designed to absorb change.
The Core Insight
Coupled code is not code that was written badly. It is code where decisions about different concerns were made in the same place. Every time you change one concern, you risk disturbing the others. The more concerns share a location, the more rigid the code becomes.
## Chapter 2: The Two Kinds of Code
Every program you have ever written, or ever will write, contains exactly two kinds of code. This is not a theoretical claim. It is an observable fact about all software, regardless of language, domain, or complexity.
Decision code is where your program’s unique logic lives. The business rules. The transformations. The calculations. The things that make your program yours and not a generic template. In a label printing program, decision code answers questions like: how do we calculate position on the page? What order should the labels appear in? How do we handle records that are too long to fit?
Plumbing code is everything that moves data from one place to another. Reading files. Writing files. Parsing formats. Rendering output. Handling HTTP requests. Connecting to databases. Plumbing code does not embody any of your program’s unique logic — it is the generic infrastructure that your decisions operate on top of.
The fundamental problem with coupled code is that these two kinds are mixed together. A single function both reads data from a file (plumbing) and decides how to transform it (decision). A single block both calculates label positions (decision) and renders them to PDF (plumbing).
When they are mixed, you cannot change one without touching the other. Want to switch from CSV to Excel? You have to edit the same function that contains your layout logic. Want to change the layout? You have to be careful not to break the file reading. Every change is a surgery where you might nick an artery.
When they are separate, changing one has zero impact on the other. Your layout logic does not know or care where the data came from. Your file parser does not know or care what happens to the data after it is read. Each piece can be understood, tested, and modified in isolation.
This separation is the entire essence of what people mean by "decoupled architecture." Everything else — hexagonal, ports and adapters, clean architecture, DDD — is just different ways of formalizing this one idea. You do not need any of that formalism. You just need to keep the two kinds apart.
# Part Two
The Mental Model
## Chapter 3: Decisions vs. Plumbing — The Only Rule You Need
The rule is simple to state: every function should either make a decision or perform plumbing, never both.
A decision function takes data in and returns data out. It does not read files, write files, call APIs, print to the screen, or interact with the outside world in any way. It is pure computation. Given the same inputs, it always produces the same outputs.
A plumbing function moves data between the outside world and your decision functions. It reads a file and converts the raw content into data structures your decision functions understand. It takes the output of a decision function and writes it to a PDF. It receives an HTTP request and translates it into the parameters a decision function expects.
Here is the discipline in concrete terms:
# DECISION function — pure, no I/O
def calculate_label_positions(labels, page_width, page_height, cols, rows):
positions = []
cell_w = page_width / cols
cell_h = page_height / rows
for i, label in enumerate(labels):
col = i % cols
row = i // cols
positions.append(Position(
x=col * cell_w,
y=row * cell_h,
width=cell_w,
height=cell_h,
content=label
))
return positions
# PLUMBING function — I/O only, no decisions
def render_labels_to_pdf(positions, output_path):
pdf = create_pdf()
for pos in positions:
pdf.draw_text(pos.x, pos.y, pos.content)
pdf.save(output_path)
Notice what happened. The calculation of where labels go is completely independent of the fact that we are writing a PDF. The PDF rendering is completely independent of how positions were calculated. If you want to change the layout algorithm, you edit one function. If you want to switch to a different PDF library, you edit the other. Neither change touches both.
This is the mental shift you are looking for. Before writing any code — or before asking an LLM to write any code — ask yourself: "Is this a decision, or is this plumbing?" If the answer is "both," you have found a place where coupling will grow.
The Litmus Test
Can you call this function in a test without any files, databases, network connections, or UI? If yes, it is a decision function and it is properly decoupled. If no, it contains plumbing that should be extracted.
## Chapter 4: A Real Example — The Avery Label Program
Let us walk through a real program from start to finish: an imposition tool that reads data from a CSV or Excel file and produces a PDF laid out as Avery 5160 labels (30 per sheet, 3 columns by 10 rows). This is the exact kind of program that feels like "it’s all plumbing" — but it is not. There are decisions hiding everywhere.
Step 1: Identify the decisions.
Before writing any code, before thinking about file formats or PDF libraries, list the decisions your program needs to make:
Parsing decisions: which columns from the spreadsheet contain which fields? What do we do with empty rows? How do we handle missing data?
Sorting decisions: what order should labels appear in? By name? By ZIP code? By row order in the file?
Formatting decisions: how do we format an address for a label? Do we abbreviate state names? How do we handle long lines?
Layout decisions: what are the exact dimensions and margins for Avery 5160? Where does each label sit on the page? When do we start a new page?
Overflow decisions: what happens when the text is too long for a label? Truncate? Shrink font? Wrap?
Every single one of these is a decision that can be implemented as a pure function. None of them require reading a file or generating a PDF. They just transform data.
Step 2: Define the data shapes.
Before any logic, define the plain data structures that will flow between your functions:
@dataclass
class RawRecord:
fields: dict[str, str]    # raw key-value pairs from spreadsheet

@dataclass
class Label:
lines: list[str]          # formatted text lines for the label

@dataclass
class LabelPosition:
page: int
row: int
col: int
x: float                  # x position in points
y: float                  # y position in points
width: float
height: float
label: Label

@dataclass
class SheetSpec:
name: str                 # e.g. 'Avery 5160'
page_width: float         # in points (72 per inch)
page_height: float
columns: int
rows: int
label_width: float
label_height: float
top_margin: float
left_margin: float
h_gap: float              # horizontal gap between labels
v_gap: float              # vertical gap between labels
These dataclasses know nothing about CSV, Excel, or PDF. They are just shapes that describe data. This is the boundary layer — the contract between your decision code and your plumbing code.
Step 3: Write the decision functions.
Now write the pure logic. Each function takes data in and returns data out. No imports of openpyxl, reportlab, or any I/O library.
# formatting.py — pure decisions, no I/O

def format_address_label(record: RawRecord, field_map: dict) -> Label:
"""Transform a raw record into formatted label lines."""
name = record.fields.get(field_map.get("name", "Name"), "")
street = record.fields.get(field_map.get("street", "Street"), "")
city = record.fields.get(field_map.get("city", "City"), "")
state = record.fields.get(field_map.get("state", "State"), "")
zip_code = record.fields.get(field_map.get("zip", "Zip"), "")

city_state_zip = f"{city}, {state} {zip_code}".strip()
lines = [l for l in [name, street, city_state_zip] if l.strip()]
return Label(lines=lines)


def sort_labels(labels: list[Label], sort_key: str = 'name') -> list[Label]:
"""Sort labels by a given criterion."""
if sort_key == 'zip':
return sorted(labels, key=lambda l: l.lines[-1] if l.lines else '')
return sorted(labels, key=lambda l: l.lines[0] if l.lines else '')
# layout.py — pure decisions, no I/O

AVERY_5160 = SheetSpec(
name='Avery 5160',
page_width=612,        # 8.5 inches
page_height=792,       # 11 inches
columns=3,
rows=10,
label_width=189.0,     # 2.625 inches
label_height=72.0,     # 1 inch
top_margin=36.0,       # 0.5 inch
left_margin=13.5,      # 0.1875 inch
h_gap=10.08,           # gap between columns
v_gap=0,               # no vertical gap on 5160
)


def assign_positions(labels: list[Label], spec: SheetSpec) -> list[LabelPosition]:
"""Place labels onto pages according to the sheet specification."""
labels_per_page = spec.columns * spec.rows
positions = []

for i, label in enumerate(labels):
page = i // labels_per_page
idx_on_page = i % labels_per_page
col = idx_on_page % spec.columns
row = idx_on_page // spec.columns

x = spec.left_margin + col * (spec.label_width + spec.h_gap)
y = spec.top_margin + row * (spec.label_height + spec.v_gap)

positions.append(LabelPosition(
page=page, row=row, col=col,
x=x, y=y,
width=spec.label_width,
height=spec.label_height,
label=label,
))

return positions
Notice: we have now implemented the entire intellectual core of the program. We can calculate label positions, format addresses, sort them — all without ever reading a file or generating a PDF. And we can test every bit of it:
# test_layout.py

def test_30_labels_fit_on_one_page():
labels = [Label(lines=['Test']) for _ in range(30)]
positions = assign_positions(labels, AVERY_5160)
assert all(p.page == 0 for p in positions)

def test_31st_label_goes_to_page_two():
labels = [Label(lines=['Test']) for _ in range(31)]
positions = assign_positions(labels, AVERY_5160)
assert positions[30].page == 1
assert positions[30].row == 0
assert positions[30].col == 0

def test_label_positions_match_avery_spec():
labels = [Label(lines=['A']), Label(lines=['B']), Label(lines=['C'])]
positions = assign_positions(labels, AVERY_5160)
assert positions[0].x == 13.5        # first column
assert positions[1].x == 212.58      # second column
assert positions[2].x == 411.66      # third column
These tests run in milliseconds, require no files, and verify the actual logic of your program. If an LLM breaks the layout algorithm, you know immediately.
Step 4: Write thin plumbing wrappers.
Only now do you involve I/O libraries. And each one is deliberately small and simple:
# readers.py — plumbing only, no decisions

import csv
import openpyxl

def read_csv(path: str) -> list[RawRecord]:
with open(path) as f:
reader = csv.DictReader(f)
return [RawRecord(fields=dict(row)) for row in reader]

def read_excel(path: str, sheet_name: str = None) -> list[RawRecord]:
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb[sheet_name] if sheet_name else wb.active
headers = [cell.value for cell in ws[1]]
records = []
for row in ws.iter_rows(min_row=2, values_only=True):
fields = {h: str(v or '') for h, v in zip(headers, row)}
records.append(RawRecord(fields=fields))
return records
# writer.py — plumbing only, no decisions

from reportlab.pdfgen import canvas

def render_pdf(positions: list[LabelPosition], output_path: str,
font_name: str = 'Helvetica', font_size: int = 10):
c = canvas.Canvas(output_path)
current_page = -1

for pos in positions:
if pos.page != current_page:
if current_page >= 0:
c.showPage()
current_page = pos.page

c.setFont(font_name, font_size)
text_y = 792 - pos.y - 14  # flip Y axis for PDF
for i, line in enumerate(pos.label.lines):
c.drawString(pos.x + 5, text_y - (i * 12), line)

c.showPage()
c.save()
Each plumbing function is short, obvious, and does exactly one thing. If you want to switch from reportlab to fpdf2 or WeasyPrint, you rewrite one function. The layout logic, the formatting, the sorting — none of it changes.
Step 5: The orchestrator ties it together.
# main.py — the dumb orchestrator

def make_labels(input_path, output_path, sort_by='name', field_map=None):
# Plumbing: read the input
if input_path.endswith('.csv'):
records = read_csv(input_path)
else:
records = read_excel(input_path)

# Decision: format each record into a label
labels = [format_address_label(r, field_map or {}) for r in records]

# Decision: sort them
labels = sort_labels(labels, sort_by)

# Decision: assign positions on pages
positions = assign_positions(labels, AVERY_5160)

# Plumbing: render to PDF
render_pdf(positions, output_path)
Look at how simple this is. It is essentially a recipe: read, format, sort, position, render. Each step is one line calling into a dedicated module. The orchestrator itself contains no logic and no I/O details. It is the table of contents for your program.
And now adding a CLI or web interface is trivial — it is just a different way of calling make_labels:
# cli.py — thin interface
if __name__ == '__main__':
import sys
make_labels(sys.argv[1], sys.argv[2])

# Or a web endpoint:
# @app.post('/labels')
# def handle(req):
#     make_labels(req.files['input'], '/tmp/output.pdf')
#     return send_file('/tmp/output.pdf')
What Just Happened
We built the entire intellectual core of the program without touching any file format or PDF library. We tested it thoroughly with pure function calls. Only at the end did we wrap it in thin plumbing. The interface — CLI, web, whatever — is a five-line afterthought. This is what decoupled feels like.
# Part Three
The Five Practices
The mental model of decisions vs. plumbing gives you the principle. These five practices give you the discipline to apply it consistently, especially when working with LLMs.
## Chapter 5: Files Are Your Architecture
The single most effective architectural decision you can make is also the simplest: put different concerns in different files.
This sounds almost too obvious to state, but it is the practice most often violated when building with LLMs. The default behavior of an LLM, when asked to build something, is to produce one file. One file that does everything. And once everything is in one file, it is psychologically and technically much harder to separate.
Files work as an architectural boundary for three reasons that are specific to working with LLMs:
First, files are the unit of context. When you tell an LLM to edit a file, it loads that file into its working memory. A small, focused file means the LLM is working with only the relevant code. A large, everything file means the LLM must hold unrelated code in memory, increasing the chance of unintended changes.
Second, files enforce import discipline. If your layout logic is in layout.py and your PDF rendering is in writer.py, the only way they can communicate is through explicit imports and function calls. This makes the dependencies visible and intentional. In a single file, any function can call any other function or access any variable with no friction at all — which is exactly what causes coupling.
Third, files are the unit of human navigation. When your codebase is twenty files of fifty lines each, you can look at the file names and immediately understand the structure. When it is one file of a thousand lines, you must read the code to understand the structure. This matters both for you and for the LLM.
A good rule of thumb: if you find yourself scrolling to find a function, or if a file has multiple sections separated by comment blocks, it should be multiple files.
Here is what the label program looks like as a file structure:
label_maker/
models.py         — dataclasses (RawRecord, Label, Position, SheetSpec)
formatting.py     — format_address_label, truncate_line
layout.py         — assign_positions, AVERY_5160
readers.py        — read_csv, read_excel
writer.py         — render_pdf
main.py           — make_labels orchestrator
cli.py            — argument parsing, calls make_labels
tests/
test_formatting.py
test_layout.py
Eight files. Each under 60 lines. Each with one job. Each independently editable by an LLM without risk to the others.
## Chapter 6: Plain Data at Every Boundary
The dataclasses from the label example are not just convenient. They are the mechanism that prevents coupling from creeping back in.
Here is what goes wrong without them. Suppose your reader function returns a pandas DataFrame instead of a list of RawRecords. Now every downstream function — formatting, sorting, layout — must understand pandas. They import pandas. They use DataFrame methods. They are coupled to a library choice that has nothing to do with their actual job.
Or suppose your formatting function returns a reportlab Paragraph object instead of a Label dataclass. Now your layout logic must understand reportlab. Your tests need reportlab installed. Your sorting function must handle reportlab objects.
Plain data structures — dataclasses, named tuples, typed dicts — act as a firewall between concerns. They define a contract: "I will give you data in this shape. I do not care how you produced it. You do not care what I will do with it."
This is the one idea worth stealing from hexagonal architecture. In the jargon, these data structures are called "ports." You do not need to know that word or use it. Just know this:
The Boundary Rule
When data crosses from one file to another, it should be a plain data object that belongs to your program, not an object that belongs to a library. This is what keeps your files independently replaceable.
In practice, this means you will often have a short conversion step at the plumbing layer. Your CSV reader does not return raw csv.DictReader rows — it converts them to RawRecords. Your PDF writer does not accept Label objects — it accepts LabelPositions that have already been computed. The conversion is trivial, usually one or two lines, but it is what keeps the decision code pure.
## Chapter 7: Tests Are Your First Interface
This is perhaps the hardest practice to internalize because it feels backward. We are trained to think "first build the thing, then test it." The discipline here is the opposite: write the test first, because the test is how you use the program before any UI exists.
This is not test-driven development dogma. It is a practical observation about how LLM-assisted development works best. When you ask an LLM to "build a label maker," it immediately reaches for file I/O and PDF generation because those are the visible outputs. But if you instead ask it to "write a function that takes a list of Label objects and returns a list of LabelPosition objects, with tests," it produces a pure function that you can verify immediately.
Tests serve three critical functions in LLM-assisted development:
Tests are executable specifications. Instead of describing what you want in natural language (which is ambiguous), a test says exactly what the input is and exactly what the output should be. When you hand this to an LLM, there is no room for misinterpretation.
Tests are regression detectors. When you ask an LLM to add a feature, existing tests will catch if it breaks something. Without tests, you are relying on manually checking everything after every change. This does not scale.
Tests force decoupling. If you cannot write a test for a function without setting up a database, creating temporary files, and starting a web server, that function is too coupled. The difficulty of testing is a direct measure of coupling. When you write tests first, you are forced to design functions that can be called in isolation.
Here is the workflow that works:
Define data shapes. Write the dataclasses that represent your domain.
Write tests for the decisions. "Given these inputs, I expect these outputs."
Ask the LLM to implement the decision functions. Point it at the test file and say "make these pass."
Add plumbing. Thin readers and writers that convert between external formats and your data shapes.
Add an orchestrator. Wire the pieces together.
Add an interface last. CLI, web, whatever — it is just a call into the orchestrator.
## Chapter 8: The Dumb Orchestrator
The orchestrator is the function that wires your decision code and plumbing code together. It has a specific character: it should be dumb. It should contain no logic of its own. It should read like a recipe.
The purpose of the dumb orchestrator is to give you (and the LLM) one place to see the entire flow of your program without being distracted by the details of any step. When you read the orchestrator, you should understand what the program does, not how it does it.
A good orchestrator looks like this:
def process_invoice(invoice_path, template_path, output_path):
raw_data = read_invoice(invoice_path)          # plumbing
validated = validate_line_items(raw_data)       # decision
totals = calculate_totals(validated)            # decision
tax = apply_tax_rules(totals, raw_data.state)  # decision
template = load_template(template_path)         # plumbing
render_invoice(template, validated, tax, output_path)  # plumbing
Six lines. Each line is one step. Each step delegates to a function in another file. The orchestrator is the skeleton; the other files are the muscles.
When you want to add a step — say, applying a discount before tax — you add one line and one function in the appropriate file. When you want to change how tax is calculated, you go to the tax function. The orchestrator barely changes over the lifetime of the program.
The mistake to watch for: putting conditional logic in the orchestrator. The moment you add an if/else to the orchestrator, you are mixing decision code in. Move that if/else into a decision function that returns the right behavior, and call that function from the orchestrator.
## Chapter 9: Side Effects at the Edges
A side effect is anything that interacts with the world outside your program: reading a file, writing a file, sending an email, making a network request, printing to the console, getting the current time. Side effects are where bugs hide, where tests become hard, and where coupling grows.
The discipline is to push side effects to the outermost edges of your program. The core should be pure computation. Side effects happen at the beginning (reading input) and at the end (writing output). The middle is entirely pure.
Visualize it as a sandwich:
PLUMBING (read)          ← side effects here
DECISION (process)     ← pure, no side effects
DECISION (transform)   ← pure, no side effects
DECISION (validate)    ← pure, no side effects
PLUMBING (write)          ← side effects here
This is sometimes called the "functional core, imperative shell" pattern. The core is functional: pure data in, pure data out. The shell is imperative: it interacts with the messy real world. The shell calls the core, never the other way around.
Why does this matter for LLMs specifically? Because when you point an LLM at a pure function, it cannot accidentally introduce a side effect. There are no file handles to leak, no connections to forget to close, no race conditions to create. The function is hermetically sealed. This is the safest possible context for an LLM to work in.
# Part Four
Integration Without Pain
## Chapter 10: Why Integration Breaks Things
Integration — making different parts of your program work together, or connecting your program to external systems — is where most projects fail. Not because integration is inherently hard, but because most code was not written to be integrated. It was written to be complete.
The difference is subtle but profound. Code that is "complete" works as a monolith. It handles everything internally. To integrate it with something else, you must crack it open and rewire its internals. Code that is "connectable" works as a component. It has clear inputs and outputs. To integrate it, you just plug something into those inputs or outputs.
When you have kept the five practices — separate files, plain data boundaries, tests first, dumb orchestrator, side effects at the edges — integration becomes almost trivial because your program is already built as a set of connectable components.
Consider the label maker. Right now it reads from files and writes to a PDF. Suppose you want to integrate it into a web application where users upload a spreadsheet and download the PDF. In a coupled design, this might require rewriting half the program. In our design, it requires writing one new plumbing function:
# A new reader that accepts an upload instead of a file path
def read_upload(file_bytes, filename) -> list[RawRecord]:
if filename.endswith('.csv'):
text = file_bytes.decode('utf-8')
reader = csv.DictReader(io.StringIO(text))
return [RawRecord(fields=dict(row)) for row in reader]
else:
wb = openpyxl.load_workbook(io.BytesIO(file_bytes))
# ... same as read_excel but from bytes
Everything else — the formatting, the layout, the rendering — is completely untouched. The decision code does not know that data now comes from a web upload instead of a local file. This is integration without pain.
## Chapter 11: The Adapter Pattern (Without the Ceremony)
In formal architecture, the code that converts between an external format and your internal data structures is called an "adapter." You do not need to think of it in those terms. Just think of it as a translator.
Every time your program touches the outside world, there is a translation step. Raw CSV rows become RawRecords. RawRecords become Labels. Label positions become PDF draw calls. Each translation is a small function that lives at the boundary.
The key insight is this: when you want to support a new external system, you do not modify existing code. You write a new translator. Want to read from Google Sheets instead of Excel? New translator. Want to output to a label printer API instead of PDF? New translator. The core logic never knows the difference.
This is what makes programs truly scalable in the sense that matters: not handling more load, but handling more change. Each new requirement adds a file; it does not modify existing files.
Here is a pattern that makes this concrete:
# readers.py grows by addition, not modification

def read_csv(path) -> list[RawRecord]: ...
def read_excel(path) -> list[RawRecord]: ...
def read_google_sheet(sheet_id) -> list[RawRecord]: ...   # new
def read_json_api(url) -> list[RawRecord]: ...            # new

# All return the same shape. The rest of the program
# does not know or care which one was used.
And the orchestrator adds one line to its routing:
# The orchestrator picks the right reader
if source.startswith('http'):
records = read_json_api(source)
elif source.startswith('gsheet:'):
records = read_google_sheet(source[7:])
elif source.endswith('.csv'):
records = read_csv(source)
else:
records = read_excel(source)
This is the adapter pattern with zero ceremony. No abstract base classes. No interface definitions. No dependency injection frameworks. Just functions that return the same shape.
## Chapter 12: Growing a System File by File
A well-structured program grows by adding files, not by making files bigger. This is the most reliable indicator of healthy architecture, and it is especially important when LLMs are doing the writing.
Here is why: when you add a file, existing tests continue to pass. Existing functions are not modified. The risk of regression is near zero. When you modify an existing file to add a feature, every existing function in that file is at risk of being inadvertently changed. The risk of regression is proportional to the size of the file.
Let us trace how the label maker might grow over six months of development:
Month 1: Basic CSV-to-PDF label printing. Six files, all under 50 lines.
Month 2: Add Excel support. One new function in readers.py. One line changed in the orchestrator. Everything else untouched.
Month 3: Support for Avery 5163 (shipping labels). Add one new SheetSpec constant to layout.py. No other changes.
Month 4: Custom text formatting (bold names, smaller font for city/state). Add a new file, styling.py, with pure functions for text styling decisions. The writer gains a small enhancement to apply styles. formatting.py untouched.
Month 5: Web interface. Add web.py with Flask routes. It calls make_labels. No changes to any existing file.
Month 6: Batch processing — users upload multiple files. Add batch.py with a function that calls make_labels in a loop. No changes to make_labels itself.
Notice the pattern: each month adds one or two files and changes at most one or two lines in existing files. The program went from a simple CLI tool to a web-based batch processing system, and the original decision code (formatting.py, layout.py) was never modified after it was first written and tested.
This is what "scalable" really means for a codebase. Not handling millions of requests. Handling dozens of changes without accumulating debt.
# Part Five
Working With LLMs Effectively
## Chapter 13: Prompt Patterns That Enforce Structure
LLMs do not naturally produce decoupled code. But they are remarkably good at following structural constraints when you state them explicitly. Here are prompt patterns that consistently produce well-structured output.
Pattern 1: The Constraint Prompt
State what the code must not do. Negative constraints are more effective than positive instructions because they are easier for the LLM to verify against.
"Write a module called layout.py that calculates label positions
for Avery 5160 sheets. Constraints:
- This module must NOT import any I/O libraries
- This module must NOT read or write files
- This module must NOT use print()
- All functions must take dataclasses as input and return
dataclasses as output
- Include type hints on all function signatures"
Pattern 2: The Test-First Prompt
Give the LLM tests and ask it to make them pass. This is dramatically more effective than describing behavior in English.
"Here are my tests for the layout module (test_layout.py).
Write the layout.py module that makes all these tests pass.
Do not modify the tests."
Pattern 3: The Targeted Edit Prompt
Never say "add feature X to the program." Always say "add feature X to [specific file]." This leverages the file-based architecture to keep the LLM’s context small and focused.
"In formatting.py, add a function called truncate_to_fit that
takes a Label and a maximum number of characters per line, and
returns a new Label with lines truncated. Add tests for this
function in test_formatting.py."
Pattern 4: The Architecture-First Prompt
For a new project, start by asking for structure, not code.
"I need to build a label printing program. Before writing any
code, give me:
1. The dataclasses that represent the domain
2. The file structure with one sentence describing each file
3. The signature of each function (name, parameters, return type)
Do not implement any functions yet."
This gives you a blueprint to review before any code exists. You can course-correct the architecture at the cheapest possible moment — before implementation.
Pattern 5: The Boundary Enforcement Prompt
When asking for plumbing code, explicitly name the data shapes it must produce or consume.
"Write a function read_excel that takes a file path and returns
a list[RawRecord]. Here is the RawRecord dataclass: [paste it].
The function should handle missing values by defaulting to empty
strings. It should not do any formatting or validation — just
return the raw data as RawRecords."
## Chapter 14: The Iterative Build Cycle
Here is the cycle that produces the best results when building with LLMs. It may feel slow at first, but it is dramatically faster than the alternative of building a monolith and then trying to untangle it later.
Phase 1: Design (10 minutes, no code)
On paper or in your head, answer three questions: What are the decisions this program makes? What data flows between those decisions? What external systems does it touch?
Phase 2: Data shapes (5 minutes, LLM-assisted)
Ask the LLM to write the dataclasses. Review them. These are the foundation and the hardest thing to change later, so get them right. Ask yourself: does each dataclass represent one concept? Could I explain what each field means to someone in thirty seconds?
Phase 3: Core logic with tests (30 minutes, LLM writes, you review)
Work through the decision functions one at a time. For each: write a few test cases (or ask the LLM to suggest test cases, then review them). Then ask the LLM to implement the function. Run the tests. If they fail, show the LLM the error and iterate.
Phase 4: Plumbing (15 minutes, LLM-assisted)
Ask the LLM to write the readers and writers. These are usually straightforward library usage and the LLM excels at this kind of code. Verify by running end-to-end with sample data.
Phase 5: Orchestrator (5 minutes)
Wire it together. This should be a few lines. If the orchestrator is complex, something in the design is wrong.
Phase 6: Interface (10 minutes, optional)
Add a CLI, web endpoint, or whatever you need. This should be a thin wrapper around the orchestrator.
Total time for a working, well-structured program: about 75 minutes. Compare this to building a monolith in 30 minutes and then spending four hours over the next week trying to add features to it.
## Chapter 15: When to Refactor and When to Rewrite
Even with good practices, you will sometimes end up with code that has grown coupled. This is normal. The question is what to do about it.
Refactor when: the overall structure is sound but one or two files have grown too large or taken on too many responsibilities. The fix is to extract functions into new files. Ask the LLM: "Extract all the pricing-related functions from orders.py into a new file called pricing.py. Update the imports in orders.py."
Rewrite when: the data shapes are wrong. If your fundamental dataclasses do not represent the domain correctly — if you find yourself constantly working around their structure — it is faster to redesign the shapes and rewrite the functions than to patch around them. With the practices from this guide, a rewrite is fast because each function is small and independently implementable.
Do nothing when: the coupling is in the plumbing layer. Messy file-reading code that works correctly is not worth refactoring. Plumbing code is inherently coupled to external libraries. As long as it produces the right data shapes at its boundary, its internal messiness is contained and harmless.
The key insight here is that the data shapes are the load-bearing structure of your program. If they are right, everything else can be refactored incrementally. If they are wrong, no amount of refactoring will fix the structural problems.
# Appendix
The Checklist
Use this checklist every time you start a new program or add a major feature to an existing one. Print it. Tape it to your monitor. Over time, these checks will become second nature and you will not need the list. But until then, the list is your discipline.
Before Writing Any Code
☐  Can I list the decisions this program makes, separate from the I/O it performs?
☐  Have I defined the data shapes (dataclasses) that flow between functions?
☐  Does each data shape represent exactly one concept?
☐  Can I describe the program’s flow in five to eight plain-English steps?
When Asking an LLM to Write Code
☐  Am I pointing it at a specific file, not the whole program?
☐  Have I stated what the function must NOT import or do?
☐  Have I specified the input and output types?
☐  Have I provided or requested tests?
☐  Is the target function under 50 lines? If not, can it be split?
When Reviewing Generated Code
☐  Does each function either make a decision OR perform I/O, never both?
☐  Can I test the decision functions without any files, databases, or network?
☐  Do functions communicate through plain data structures, not framework objects?
☐  Is the orchestrator dumb — just sequencing calls with no embedded logic?
☐  Are side effects only at the very beginning and very end of the flow?
When Adding Features
☐  Am I adding a new file, or modifying an existing one? (Prefer adding.)
☐  If modifying, am I touching only one file? If more, is the data shape changing?
☐  Do existing tests still pass without modification?
☐  Is the orchestrator still dumb after this change?
Remember: decoupling is not an architecture you adopt once. It is a discipline you apply with every function, every file, every prompt you give to an LLM. The goal is not perfect architecture. The goal is code that stays soft — code that welcomes change instead of resisting it.

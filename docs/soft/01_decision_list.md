# Step 1: Decision List

Goal: Identify all *decisions* this tool makes. No plumbing.

## Output
Create `core/<tool>/DECISIONS.md` with:
- A short summary of the tool
- A bullet list of decisions (pure logic)

## Rules
- No mention of file formats, databases, or frameworks.
- Each item should be testable without IO.

## Example
- How to filter blank records
- How to position labels
- How to handle overflow text

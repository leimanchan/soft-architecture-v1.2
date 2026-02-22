const sessionData = {
    sessionId: null,
    sheetName: null,
    sheetNames: [],
    columns: [],
    totalRows: 0,
    labelFields: []
};

let selectedField = null;
const POSITION_MIN = 0;
const POSITION_MAX = 1;
const POSITION_STEP = 0.02;

const uploadSpinner = document.getElementById('uploadSpinner');
const uploadStatus = document.getElementById('uploadStatus');
const sheetSelector = document.getElementById('sheetSelector');
const previewContainer = document.getElementById('previewContainer');
const sheetSelect = document.getElementById('sheetSelect');
const sheetSelectEditor = document.getElementById('sheetSelectEditor');
const dataPreview = document.getElementById('dataPreview');
const totalRows = document.getElementById('totalRows');
const editorTotalRows = document.getElementById('editorTotalRows');
const editorSheetStatus = document.getElementById('editorSheetStatus');
const editorSheetBar = document.getElementById('editorSheetBar');
const fieldList = document.getElementById('fieldList');
const addedFieldsList = document.getElementById('addedFieldsList');
const fieldControls = document.getElementById('fieldControls');
const generateSpinner = document.getElementById('generateSpinner');
const generateStatus = document.getElementById('generateStatus');

const loadSheetBtn = document.getElementById('loadSheetBtn');
const loadSheetEditorBtn = document.getElementById('loadSheetEditorBtn');
const toDesignBtn = document.getElementById('toDesignBtn');
const backBtn = document.getElementById('backBtn');
const resetBtn = document.getElementById('resetBtn');
const withTemplateBtn = document.getElementById('withTemplateBtn');
const generateBtn = document.getElementById('generateBtn');
const restartBtn = document.getElementById('restartBtn');
const addWorksheetBtn = document.getElementById('addWorksheetBtn');
const addCustomBtn = document.getElementById('addCustomBtn');

function setStep(step) {
    document.querySelectorAll('.step').forEach(el => el.classList.remove('is-active'));
    document.querySelectorAll('.progress-step').forEach(el => {
        el.classList.remove('is-active', 'is-complete');
    });

    const stepEl = document.getElementById(`step${step}`);
    if (stepEl) {
        stepEl.classList.add('is-active');
    }

    for (let i = 1; i <= 3; i += 1) {
        const progressStep = document.querySelector(`.progress-step[data-step="${i}"]`);
        if (!progressStep) continue;
        if (i < step) {
            progressStep.classList.add('is-complete');
        } else if (i === step) {
            progressStep.classList.add('is-active');
        }
    }

    if (step === 2) {
        initializeDesigner();
        if (editorSheetBar) {
            editorSheetBar.style.display = 'flex';
        }
    }
}

function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status ${type}`;
    element.style.display = 'block';
}

function hideStatus(element) {
    element.style.display = 'none';
}

async function handleUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadSpinner.style.display = 'block';
    hideStatus(uploadStatus);

    try {
        const response = await fetch('upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (data.error) {
            showStatus(uploadStatus, data.error, 'error');
            return;
        }

        sessionData.sessionId = data.session_id;
        sessionData.sheetNames = data.sheet_names;
        populateSheetSelectors();
        sheetSelector.style.display = 'block';
    } catch (error) {
        showStatus(uploadStatus, `Upload failed: ${error.message}`, 'error');
    } finally {
        uploadSpinner.style.display = 'none';
    }
}

function populateSheetSelectors() {
    if (sheetSelect) sheetSelect.innerHTML = '';
    if (sheetSelectEditor) sheetSelectEditor.innerHTML = '';

    sessionData.sheetNames.forEach(name => {
        const optionA = document.createElement('option');
        optionA.value = name;
        optionA.textContent = name;
        if (sheetSelect) sheetSelect.appendChild(optionA);

        const optionB = document.createElement('option');
        optionB.value = name;
        optionB.textContent = name;
        if (sheetSelectEditor) sheetSelectEditor.appendChild(optionB);
    });

    if (sessionData.sheetName) {
        if (sheetSelect) sheetSelect.value = sessionData.sheetName;
        if (sheetSelectEditor) sheetSelectEditor.value = sessionData.sheetName;
    }
}

async function loadSheet(selectId = 'sheetSelect') {
    const selectElement = document.getElementById(selectId);
    if (!selectElement) {
        showStatus(uploadStatus, 'Worksheet selector is unavailable. Please reload the page.', 'error');
        return;
    }

    const sheetName = selectElement.value;
    if (!sheetName) return;
    const isEditor = selectId === 'sheetSelectEditor';
    const previousSheet = sessionData.sheetName;

    uploadSpinner.style.display = 'block';
    if (editorSheetStatus) editorSheetStatus.textContent = '';

    try {
        const response = await fetch('load_sheet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionData.sessionId,
                sheet_name: sheetName
            })
        });
        const data = await response.json();

        if (data.error) {
            showStatus(uploadStatus, data.error, 'error');
            return;
        }

        sessionData.sheetName = sheetName;
        sessionData.columns = data.columns;
        sessionData.totalRows = data.total_rows;
        displayPreview(data.preview, data.columns);
        totalRows.textContent = data.total_rows;

        if (!isEditor) {
            sheetSelector.style.display = 'none';
            previewContainer.style.display = 'block';
        }

        if (editorSheetBar) editorSheetBar.style.display = 'flex';
        if (editorTotalRows) editorTotalRows.textContent = data.total_rows;
        if (editorSheetStatus) editorSheetStatus.textContent = 'Updated';
        populateSheetSelectors();

        if (previousSheet && previousSheet !== sheetName) {
            const nextColumns = new Set(sessionData.columns);
            const seenColumns = new Set();
            const previousCount = sessionData.labelFields.length;

            sessionData.labelFields = sessionData.labelFields.filter(field => {
                if (field.is_static) {
                    if (field.column === previousSheet) {
                        field.column = sheetName;
                        field.static_text = sheetName;
                    }
                    return true;
                }

                if (!nextColumns.has(field.column) || seenColumns.has(field.column)) {
                    return false;
                }

                seenColumns.add(field.column);
                return true;
            });

            if (selectedField !== null && selectedField >= sessionData.labelFields.length) {
                selectedField = null;
            }

            const removedCount = previousCount - sessionData.labelFields.length;
            if (removedCount > 0 && editorSheetStatus) {
                editorSheetStatus.textContent = `Updated (removed ${removedCount} incompatible field${removedCount === 1 ? '' : 's'})`;
            }
        }

        if (isEditor || document.getElementById('step2').classList.contains('is-active')) {
            initializeDesigner();
            renderLabelPreview();
            renderFieldControls();
        }
    } catch (error) {
        showStatus(uploadStatus, `Error: ${error.message}`, 'error');
        if (editorSheetStatus) editorSheetStatus.textContent = 'Error loading worksheet';
    } finally {
        uploadSpinner.style.display = 'none';
    }
}

function displayPreview(data, columns) {
    let html = '<table><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            html += `<td>${row[col] !== null ? row[col] : ''}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    dataPreview.innerHTML = html;
}

function initializeDesigner() {
    fieldList.innerHTML = '';
    sessionData.columns.forEach(column => {
        const fieldItem = document.createElement('div');
        fieldItem.className = 'field-item';
        fieldItem.textContent = column;
        fieldItem.addEventListener('click', () => addFieldToLabel(column));
        fieldList.appendChild(fieldItem);
    });
}

function addFieldToLabel(column) {
    if (sessionData.labelFields.find(f => !f.is_static && f.column === column)) {
        return;
    }

    const field = {
        column,
        align: 'center',
        y: 0.35 + (sessionData.labelFields.length * 0.32),
        font_family: 'Helvetica',
        font_weight: 'Regular',
        size: 25,
        letter_spacing: 0,
        prefix: '',
        suffix: '',
        is_header: false,
        is_static: false
    };

    sessionData.labelFields.push(field);
    renderLabelPreview();
}

function addStaticField(type) {
    let text = '';
    if (type === 'worksheet') {
        text = sessionData.sheetName || 'Sheet Name';
    } else {
        const input = document.getElementById('customTextInput');
        text = input.value.trim();
        if (!text) {
            alert('Please enter custom text first');
            return;
        }
        input.value = '';
    }

    const field = {
        column: text,
        static_text: text,
        align: 'center',
        y: 0.35 + (sessionData.labelFields.length * 0.4),
        font_family: 'Helvetica',
        font_weight: 'Bold',
        size: 25,
        letter_spacing: 1,
        is_header: true,
        is_static: true
    };

    sessionData.labelFields.push(field);
    renderLabelPreview();
}

function renderLabelPreview() {
    addedFieldsList.innerHTML = '';

    if (sessionData.labelFields.length === 0) {
        const empty = document.createElement('p');
        empty.className = 'empty-state';
        empty.textContent = 'Click fields on the left to add them to your label.';
        addedFieldsList.appendChild(empty);
        return;
    }

    sessionData.labelFields.forEach((field, index) => {
        const fieldEl = document.createElement('div');
        fieldEl.className = 'added-field';
        if (selectedField === index) {
            fieldEl.classList.add('is-selected');
        }

        const fieldName = document.createElement('div');
        fieldName.className = 'field-name';
        fieldName.textContent = field.is_static ? `Static: ${field.column}` : field.column;

        const fieldPosition = document.createElement('div');
        fieldPosition.className = 'field-position';
        fieldPosition.innerHTML = `
            <div class="position-controls">
                <button type="button" class="position-btn position-btn-up" aria-label="Move ${field.column} up">Move Up</button>
                <div class="position-readout">
                    <span class="position-value">${field.y.toFixed(2)} in</span>
                    <span class="position-help">Up reduces Y</span>
                </div>
                <button type="button" class="position-btn position-btn-down" aria-label="Move ${field.column} down">Move Down</button>
            </div>
        `;

        const upBtn = fieldPosition.querySelector('.position-btn-up');
        upBtn.addEventListener('click', event => {
            event.stopPropagation();
            nudgeFieldPosition(index, -POSITION_STEP);
        });

        const downBtn = fieldPosition.querySelector('.position-btn-down');
        downBtn.addEventListener('click', event => {
            event.stopPropagation();
            nudgeFieldPosition(index, POSITION_STEP);
        });

        fieldEl.appendChild(fieldName);
        fieldEl.appendChild(fieldPosition);
        fieldEl.addEventListener('click', () => selectField(index));

        addedFieldsList.appendChild(fieldEl);
    });
}

function updateFieldPosition(index, yPos) {
    const clamped = Math.max(POSITION_MIN, Math.min(POSITION_MAX, yPos));
    sessionData.labelFields[index].y = parseFloat(clamped.toFixed(2));
    renderLabelPreview();
}

function nudgeFieldPosition(index, delta) {
    const current = Number(sessionData.labelFields[index].y) || 0;
    updateFieldPosition(index, current + delta);
}

function selectField(index) {
    selectedField = index;
    renderLabelPreview();
    renderFieldControls();
}

function renderFieldControls() {
    if (selectedField === null) {
        fieldControls.innerHTML = '<p class="empty-state">Select a label field to edit its settings.</p>';
        return;
    }

    const field = sessionData.labelFields[selectedField];
    const isStatic = field.is_static;

    fieldControls.innerHTML = `
        <div class="control-group">
            <label>${isStatic ? 'Static Text' : 'Data Field'}: <strong>${field.column}</strong></label>
        </div>
        <div class="control-group">
            <label>Text Alignment</label>
            <select id="alignSelect">
                <option value="left">Left</option>
                <option value="center">Center</option>
                <option value="right">Right</option>
            </select>
        </div>
        <div class="control-group">
            <label>Font Family</label>
            <select id="fontFamilySelect">
                <option value="Helvetica">Helvetica</option>
                <option value="Times">Times New Roman</option>
                <option value="Courier">Courier</option>
            </select>
        </div>
        <div class="control-group">
            <label>Font Weight</label>
            <select id="fontWeightSelect">
                <option value="Regular">Regular</option>
                <option value="Bold">Bold</option>
            </select>
        </div>
        <div class="control-group">
            <label>Max Font Size</label>
            <input type="number" id="fontSizeInput" min="6" max="36" value="${field.size}">
        </div>
        <div class="control-group">
            <label>Letter Spacing</label>
            <input type="number" id="letterSpacingInput" min="-2" max="5" step="0.5" value="${field.letter_spacing || 0}">
        </div>
        ${isStatic ? '' : `
        <div class="control-group">
            <label>Text Before (Prefix)</label>
            <input type="text" id="prefixInput" value="${field.prefix || ''}" placeholder="e.g., Player: ">
        </div>
        <div class="control-group">
            <label>Text After (Suffix)</label>
            <input type="text" id="suffixInput" value="${field.suffix || ''}" placeholder="e.g., pts">
        </div>
        `}
        <div class="control-group">
            <label class="checkbox-row">
                <input type="checkbox" id="headerToggle" ${field.is_header ? 'checked' : ''}>
                <span>Header Style (Green, Bold, Underlined, CAPS)</span>
            </label>
        </div>
        <div class="control-group">
            <button class="btn btn-secondary" id="removeFieldBtn">Remove Field</button>
        </div>
    `;

    const alignSelect = document.getElementById('alignSelect');
    alignSelect.value = field.align || 'left';
    alignSelect.addEventListener('change', e => updateField('align', e.target.value));

    const fontFamilySelect = document.getElementById('fontFamilySelect');
    fontFamilySelect.value = field.font_family || 'Helvetica';
    fontFamilySelect.addEventListener('change', e => updateField('font_family', e.target.value));

    const fontWeightSelect = document.getElementById('fontWeightSelect');
    fontWeightSelect.value = field.font_weight || 'Regular';
    fontWeightSelect.addEventListener('change', e => updateField('font_weight', e.target.value));

    const fontSizeInput = document.getElementById('fontSizeInput');
    fontSizeInput.addEventListener('change', e => updateField('size', parseInt(e.target.value, 10)));

    const letterSpacingInput = document.getElementById('letterSpacingInput');
    letterSpacingInput.addEventListener('change', e => updateField('letter_spacing', parseFloat(e.target.value)));

    if (!isStatic) {
        const prefixInput = document.getElementById('prefixInput');
        prefixInput.addEventListener('change', e => updateField('prefix', e.target.value));
        const suffixInput = document.getElementById('suffixInput');
        suffixInput.addEventListener('change', e => updateField('suffix', e.target.value));
    }

    const headerToggle = document.getElementById('headerToggle');
    headerToggle.addEventListener('change', e => updateField('is_header', e.target.checked));

    const removeFieldBtn = document.getElementById('removeFieldBtn');
    removeFieldBtn.addEventListener('click', removeField);
}

function updateField(prop, value) {
    if (selectedField === null) return;
    sessionData.labelFields[selectedField][prop] = value;
    renderLabelPreview();
}

function removeField() {
    if (selectedField === null) return;
    sessionData.labelFields.splice(selectedField, 1);
    selectedField = null;
    renderLabelPreview();
    renderFieldControls();
}

async function generatePDF(useTemplate = false) {
    if (sessionData.labelFields.length === 0) {
        showStatus(generateStatus, 'Please add at least one field to your label.', 'error');
        return;
    }

    const copiesPerRecord = parseInt(document.getElementById('copiesPerRecord').value, 10) || 1;

    generateSpinner.style.display = 'block';
    hideStatus(generateStatus);

    try {
        const response = await fetch('generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionData.sessionId,
                sheet_name: sessionData.sheetName,
                use_template: useTemplate,
                copies_per_record: copiesPerRecord,
                label_config: {
                    fields: sessionData.labelFields
                }
            })
        });

        if (!response.ok) {
            const error = await response.json();
            showStatus(generateStatus, error.error || 'Failed to generate PDF', 'error');
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'avery_5160_labels.pdf';
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);

        showStatus(generateStatus, 'PDF generated! Make adjustments and regenerate, or start a new label.', 'success');
    } catch (error) {
        showStatus(generateStatus, `Error: ${error.message}`, 'error');
    } finally {
        generateSpinner.style.display = 'none';
    }
}

function resetFlow() {
    window.location.reload();
}

loadSheetBtn.addEventListener('click', () => loadSheet('sheetSelect'));
if (loadSheetEditorBtn) loadSheetEditorBtn.addEventListener('click', () => loadSheet('sheetSelectEditor'));
if (sheetSelectEditor) sheetSelectEditor.addEventListener('change', () => loadSheet('sheetSelectEditor'));
toDesignBtn.addEventListener('click', () => setStep(2));
backBtn.addEventListener('click', () => setStep(1));
resetBtn.addEventListener('click', resetFlow);
withTemplateBtn.addEventListener('click', () => generatePDF(true));
generateBtn.addEventListener('click', () => generatePDF(false));
restartBtn.addEventListener('click', resetFlow);
addWorksheetBtn.addEventListener('click', () => addStaticField('worksheet'));
addCustomBtn.addEventListener('click', () => addStaticField('custom'));
document.getElementById('fileInput').addEventListener('change', handleUpload);

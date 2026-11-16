/**
 * Family Tree Suggestions Controller
 * Enables visitors and relatives to submit suggestions, corrections, and family stories.
 */

(function () {
    'use strict';

    // Configuration
    // Web3Forms access key
    var CONFIG = {
        accessKey: 'cea10819-2fe2-4273-aa54-60fa343a1d3f',
        adminEmail: 'emilkerimov93@gmail.com',
        endpoint: 'https://api.web3forms.com/submit'
    };

    var modalInjected = false;

    function buildModalHTML() {
        return [
            '<div id="ftSuggestionModal" class="ft-modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="ftModalTitle">',
            '    <div class="ft-modal-dialog">',
            '        <div class="ft-modal-header">',
            '            <div class="ft-modal-header-content">',
            '                <h3 id="ftModalTitle"><span>✏️</span> Suggest an Edit or Story</h3>',
            '                <span id="ftModalTargetBadge" class="ft-modal-target-badge">General Suggestion</span>',
            '            </div>',
            '            <button type="button" class="ft-modal-close" id="ftModalCloseBtn" title="Close modal">&times;</button>',
            '        </div>',
            '        <div class="ft-modal-body">',
            '            <div id="ftAlertError" class="ft-modal-alert ft-alert-error" role="alert"></div>',
            '            <div id="ftAlertWarning" class="ft-modal-alert ft-alert-warning" role="alert"></div>',
            '            ',
            '            <div id="ftSuccessView" class="ft-alert-success" style="display: none;">',
            '                <h4>🎉 Thank You!</h4>',
            '                <p id="ftSuccessMessage">Your suggestion has been submitted successfully to Emil for review.</p>',
            '                <button type="button" class="ft-btn ft-btn-primary" id="ftSuccessCloseBtn" style="margin-top: 14px;">Done</button>',
            '            </div>',
            '            ',
            '            <form id="ftSuggestionForm">',
            '                <!-- Hidden Web3Forms & Context Fields -->',
            '                <input type="hidden" name="person_id" id="ftPersonId" value="">',
            '                <input type="hidden" name="person_name" id="ftPersonName" value="">',
            '                <input type="hidden" name="page_url" id="ftPageUrl" value="">',
            '                <input type="checkbox" name="botcheck" id="ftBotCheck" style="display:none !important;" tabindex="-1" autocomplete="off">',
            '                ',
            '                <div class="ft-form-group">',
            '                    <label for="ftTypeSelect">What would you like to suggest? <span class="ft-req">*</span></label>',
            '                    <select id="ftTypeSelect" name="suggestion_type" class="ft-form-control" required>',
            '                        <option value="Birth / Death / Burial details">📅 Birth, Death, or Burial details (dates/places)</option>',
            '                        <option value="Spouse / Marriage details">💍 Add Spouse or Marriage information</option>',
            '                        <option value="Add Child or Parent">👶 Add Child or Parent</option>',
            '                        <option value="Occupation / Education / Military">💼 Occupation, Education, or Life Events</option>',
            '                        <option value="Family Story / Memory / Anecdote">📖 Family Story, Memory, Anecdote, or Bio</option>',
            '                        <option value="Correction to existing info">✏️ Correction to existing information</option>',
            '                        <option value="Add new person to tree">👤 Add a completely new person to the tree</option>',
            '                        <option value="Other">💬 Other notes or question</option>',
            '                    </select>',
            '                </div>',
            '                ',
            '                <div class="ft-form-group">',
            '                    <label for="ftDetails">Details or Family Story <span class="ft-req">*</span></label>',
            '                    <textarea id="ftDetails" name="details" class="ft-form-control" placeholder="Please describe the date, location, names, or family story you would like to share..." required></textarea>',
            '                </div>',
            '                ',
            '                <div class="ft-form-group">',
            '                    <label for="ftSources">Source or Evidence <span class="ft-form-hint">(Optional)</span></label>',
            '                    <input type="text" id="ftSources" name="source" class="ft-form-control" placeholder="e.g. Family memory, certificate, passport, grave inscription, letter...">',
            '                </div>',
            '                ',
            '                <div class="ft-form-row">',
            '                    <div class="ft-form-group">',
            '                        <label for="ftSubmitterName">Your Name <span class="ft-req">*</span></label>',
            '                        <input type="text" id="ftSubmitterName" name="submitter_name" class="ft-form-control" placeholder="e.g. Leyla Kerimova" required>',
            '                    </div>',
            '                    <div class="ft-form-group">',
            '                        <label for="ftSubmitterContact">Your Email or Phone <span class="ft-form-hint">(Optional)</span></label>',
            '                        <input type="text" id="ftSubmitterContact" name="submitter_contact" class="ft-form-control" placeholder="e.g. name@email.com">',
            '                    </div>',
            '                </div>',
            '                ',
            '                <div class="ft-form-group">',
            '                    <label for="ftRelationship">Your Relationship to this Person or Family <span class="ft-form-hint">(Optional)</span></label>',
            '                    <input type="text" id="ftRelationship" name="relationship" class="ft-form-control" placeholder="e.g. Granddaughter, Cousin, Son, Self, Friend">',
            '                </div>',
            '            </form>',
            '        </div>',
            '        <div class="ft-modal-footer" id="ftModalFooter">',
            '            <button type="button" class="ft-btn ft-btn-secondary" id="ftCancelBtn">Cancel</button>',
            '            <button type="button" class="ft-btn ft-btn-primary" id="ftSubmitBtn">',
            '                <span id="ftBtnSpinner" class="ft-spinner" style="display: none;"></span>',
            '                <span id="ftBtnText">Send Suggestion</span>',
            '            </button>',
            '        </div>',
            '    </div>',
            '</div>'
        ].join('\n');
    }

    function ensureModalInDOM() {
        if (modalInjected || document.getElementById('ftSuggestionModal')) {
            modalInjected = true;
            return;
        }

        var wrapper = document.createElement('div');
        wrapper.innerHTML = buildModalHTML();
        document.body.appendChild(wrapper.firstElementChild);
        modalInjected = true;
        bindModalEvents();
    }

    function bindModalEvents() {
        var modal = document.getElementById('ftSuggestionModal');
        var closeBtn = document.getElementById('ftModalCloseBtn');
        var cancelBtn = document.getElementById('ftCancelBtn');
        var submitBtn = document.getElementById('ftSubmitBtn');
        var successCloseBtn = document.getElementById('ftSuccessCloseBtn');

        if (closeBtn) closeBtn.addEventListener('click', closeSuggestionModal);
        if (cancelBtn) cancelBtn.addEventListener('click', closeSuggestionModal);
        if (successCloseBtn) successCloseBtn.addEventListener('click', closeSuggestionModal);

        if (submitBtn) {
            submitBtn.addEventListener('click', function (e) {
                e.preventDefault();
                submitSuggestion();
            });
        }

        // Close on backdrop click
        if (modal) {
            modal.addEventListener('click', function (e) {
                if (e.target === modal) {
                    closeSuggestionModal();
                }
            });
        }

        // Close on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && isModalOpen()) {
                closeSuggestionModal();
            }
        });
    }

    function isModalOpen() {
        var modal = document.getElementById('ftSuggestionModal');
        return modal && modal.classList.contains('is-active');
    }

    function openSuggestionModal(personId, personName) {
        ensureModalInDOM();

        var modal = document.getElementById('ftSuggestionModal');
        var targetBadge = document.getElementById('ftModalTargetBadge');
        var personIdInput = document.getElementById('ftPersonId');
        var personNameInput = document.getElementById('ftPersonName');
        var pageUrlInput = document.getElementById('ftPageUrl');
        var alertError = document.getElementById('ftAlertError');
        var alertWarning = document.getElementById('ftAlertWarning');
        var form = document.getElementById('ftSuggestionForm');
        var successView = document.getElementById('ftSuccessView');
        var footer = document.getElementById('ftModalFooter');

        // Reset visibility
        if (form) form.style.display = 'block';
        if (footer) footer.style.display = 'flex';
        if (successView) successView.style.display = 'none';
        if (alertError) {
            alertError.textContent = '';
            alertError.classList.remove('is-visible');
        }
        if (alertWarning) {
            alertWarning.innerHTML = '';
            alertWarning.classList.remove('is-visible');
        }

        // Set context
        var pid = (personId || '').trim();
        var pname = (personName || '').trim();

        if (pid || pname) {
            var label = pname;
            if (pid && pname) {
                label = pname + ' [' + pid + ']';
            } else if (pid) {
                label = '[' + pid + ']';
            }
            if (targetBadge) targetBadge.textContent = 'Regarding: ' + label;
        } else {
            if (targetBadge) targetBadge.textContent = 'General Family Tree Suggestion / New Person';
        }

        if (personIdInput) personIdInput.value = pid;
        if (personNameInput) personNameInput.value = pname;
        if (pageUrlInput) pageUrlInput.value = window.location.href;

        // Check if access key is configured
        if (CONFIG.accessKey === 'YOUR_ACCESS_KEY_HERE') {
            if (alertWarning) {
                alertWarning.innerHTML = '<strong>Setup Notice:</strong> Web3Forms access key is not yet configured. Once Emil adds his key to <code>CONFIG.accessKey</code>, submissions will arrive instantly via email. Submissions can also be sent via email client.';
                alertWarning.classList.add('is-visible');
            }
        }

        // Open modal
        modal.classList.add('is-active');
        document.body.style.overflow = 'hidden';

        // Focus first field
        var typeSelect = document.getElementById('ftTypeSelect');
        if (typeSelect) setTimeout(function () { typeSelect.focus(); }, 100);
    }

    function closeSuggestionModal() {
        var modal = document.getElementById('ftSuggestionModal');
        if (modal) {
            modal.classList.remove('is-active');
        }
        document.body.style.overflow = '';
        var form = document.getElementById('ftSuggestionForm');
        if (form) form.reset();
        setSubmittingState(false);
    }

    function setSubmittingState(isSubmitting) {
        var submitBtn = document.getElementById('ftSubmitBtn');
        var spinner = document.getElementById('ftBtnSpinner');
        var btnText = document.getElementById('ftBtnText');
        var cancelBtn = document.getElementById('ftCancelBtn');

        if (!submitBtn) return;

        submitBtn.disabled = isSubmitting;
        if (cancelBtn) cancelBtn.disabled = isSubmitting;
        if (spinner) spinner.style.display = isSubmitting ? 'inline-block' : 'none';
        if (btnText) btnText.textContent = isSubmitting ? 'Sending...' : 'Send Suggestion';
    }

    function submitSuggestion() {
        var form = document.getElementById('ftSuggestionForm');
        var alertError = document.getElementById('ftAlertError');
        var botCheck = document.getElementById('ftBotCheck');

        if (alertError) {
            alertError.textContent = '';
            alertError.classList.remove('is-visible');
        }

        // Spam bot check
        if (botCheck && botCheck.checked) {
            closeSuggestionModal();
            return;
        }

        var details = (document.getElementById('ftDetails').value || '').trim();
        var submitterName = (document.getElementById('ftSubmitterName').value || '').trim();
        var type = document.getElementById('ftTypeSelect').value;
        var source = (document.getElementById('ftSources').value || '').trim();
        var contact = (document.getElementById('ftSubmitterContact').value || '').trim();
        var relationship = (document.getElementById('ftRelationship').value || '').trim();
        var personId = document.getElementById('ftPersonId').value;
        var personName = document.getElementById('ftPersonName').value;
        var pageUrl = document.getElementById('ftPageUrl').value;

        if (!type || !details || !submitterName) {
            if (alertError) {
                alertError.textContent = 'Please fill out all required fields marked with an asterisk (*).';
                alertError.classList.add('is-visible');
            }
            return;
        }

        var subjectPerson = personName ? (personName + (personId ? ' [' + personId + ']' : '')) : 'General / New Person';
        var emailSubject = 'Family Tree Suggestion: ' + subjectPerson + ' (' + type + ')';

        // Build Payload
        var payload = {
            access_key: CONFIG.accessKey,
            subject: emailSubject,
            from_name: submitterName + ' (Family Tree Suggestion)',
            person_name: personName || 'General / Unlisted',
            person_id: personId || 'None',
            suggestion_type: type,
            details: details,
            source: source || 'None provided',
            submitter_name: submitterName,
            submitter_contact: contact || 'Not provided',
            submitter_relationship: relationship || 'Not specified',
            page_url: pageUrl
        };

        // If contact looks like an email, set replyto
        if (contact && contact.indexOf('@') > -1) {
            payload.replyto = contact;
        }

        // If key is placeholder, offer mailto client fallback
        if (CONFIG.accessKey === 'YOUR_ACCESS_KEY_HERE') {
            var bodyText = [
                'Hello Emil,',
                '',
                'I have a suggestion for the Family Tree:',
                '',
                'Regarding: ' + subjectPerson,
                'Category: ' + type,
                'Details: ' + details,
                'Source: ' + (source || 'N/A'),
                'My Name: ' + submitterName,
                'Contact: ' + (contact || 'N/A'),
                'Relationship: ' + (relationship || 'N/A'),
                'Page: ' + pageUrl
            ].join('\n');

            var mailtoUrl = 'mailto:' + encodeURIComponent(CONFIG.adminEmail) +
                '?subject=' + encodeURIComponent(emailSubject) +
                '&body=' + encodeURIComponent(bodyText);

            if (alertError) {
                alertError.innerHTML = 'Web3Forms access key is pending activation. <a href="' + mailtoUrl + '" style="font-weight:bold; color:#1e395b; text-decoration:underline;">Click here to send this suggestion via your email app</a>, or have Emil configure the key.';
                alertError.classList.add('is-visible');
            }
            return;
        }

        setSubmittingState(true);

        fetch(CONFIG.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            setSubmittingState(false);
            if (data.success) {
                showSuccessState(submitterName, subjectPerson);
            } else {
                showErrorState(data.message || 'Could not send suggestion. Please try again later.');
            }
        })
        .catch(function (err) {
            setSubmittingState(false);
            showErrorState('Network error occurred. Please check your connection or contact Emil directly.');
        });
    }

    function showSuccessState(submitterName, subjectPerson) {
        var form = document.getElementById('ftSuggestionForm');
        var footer = document.getElementById('ftModalFooter');
        var successView = document.getElementById('ftSuccessView');
        var successMessage = document.getElementById('ftSuccessMessage');

        if (form) form.style.display = 'none';
        if (footer) footer.style.display = 'none';
        if (successMessage) {
            successMessage.innerHTML = 'Thank you, <strong>' + escapeHtml(submitterName) + '</strong>!<br>Your suggestion regarding <strong>' + escapeHtml(subjectPerson) + '</strong> has been sent to Emil Kerimov for review.';
        }
        if (successView) successView.style.display = 'block';
    }

    function showErrorState(msg) {
        var alertError = document.getElementById('ftAlertError');
        if (alertError) {
            alertError.textContent = msg;
            alertError.classList.add('is-visible');
        }
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Global click listener for suggest links and buttons
    document.addEventListener('click', function (e) {
        var target = e.target;
        var editBtn = target.closest('.suggest-edit-link, .btn-suggest-edit');
        if (editBtn) {
            e.preventDefault();
            var pid = editBtn.getAttribute('data-person-id') || '';
            var pname = editBtn.getAttribute('data-person-name') || '';
            openSuggestionModal(pid, pname);
            return;
        }

        var generalBtn = target.closest('.suggest-general-link');
        if (generalBtn) {
            e.preventDefault();
            openSuggestionModal('', '');
            return;
        }
    });

    // Expose functions globally
    window.openSuggestionModal = openSuggestionModal;
    window.closeSuggestionModal = closeSuggestionModal;
    window.FT_SUGGESTIONS_CONFIG = CONFIG;

})();

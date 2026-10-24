/**
 * Interactive Family Tree Graph Controller
 * Powered by PeWu/topola layout engine and D3.js
 */

(function () {
    'use strict';

    let parsedGedcomJson = null;
    let familyGraph = {};
    let currentIndi = null;
    let defaultHomeIndi = null;
    let currentView = 'relatives';
    let currentColor = 'sex';
    let zoomBehavior = null;
    let svgSelection = null;
    let zoomLayer = null;
    let lastChartInfo = null;
    let selectedIndiId = null;
    let lastClickPos = { x: 100, y: 100 };
    let lastClickedIndi = null;
    let lastClickTime = 0;

    const CHART_MAP = {
        relatives: window.Topola ? Topola.RelativesChart : null,
        hourglass: window.Topola ? Topola.HourglassChart : null,
        ancestors: window.Topola ? Topola.AncestorChart : null,
        descendants: window.Topola ? Topola.DescendantChart : null
    };

    const COLOR_MAP = {
        sex: window.Topola ? Topola.ChartColors.BY_SEX : undefined,
        generation: window.Topola ? Topola.ChartColors.BY_GENERATION : undefined,
        none: window.Topola ? Topola.ChartColors.NO_COLOR : undefined
    };

    function init() {
        if (!window.Topola) {
            console.error('Topola library failed to load.');
            return;
        }

        // Initialize chart map references
        CHART_MAP.relatives = Topola.RelativesChart;
        CHART_MAP.hourglass = Topola.HourglassChart;
        CHART_MAP.ancestors = Topola.AncestorChart;
        CHART_MAP.descendants = Topola.DescendantChart;

        COLOR_MAP.sex = Topola.ChartColors.BY_SEX;
        COLOR_MAP.generation = Topola.ChartColors.BY_GENERATION;
        COLOR_MAP.none = Topola.ChartColors.NO_COLOR;

        // Parse family graph data (metadata & profile paths)
        const graphEl = document.getElementById('familyGraphData');
        if (graphEl && graphEl.textContent.trim()) {
            try {
                familyGraph = JSON.parse(graphEl.textContent);
            } catch (e) {
                console.error('Error parsing family graph JSON:', e);
            }
        }

        // Parse GEDCOM data
        const gedcomEl = document.getElementById('gedcomData');
        if (gedcomEl && gedcomEl.textContent.trim()) {
            try {
                parsedGedcomJson = Topola.gedcomToJson(gedcomEl.textContent);
            } catch (e) {
                console.error('Error parsing GEDCOM data with Topola:', e);
            }
        }

        if (!parsedGedcomJson || !parsedGedcomJson.indis || parsedGedcomJson.indis.length === 0) {
            fetch('ged/family_tree.ged')
                .then(r => r.text())
                .then(text => {
                    parsedGedcomJson = Topola.gedcomToJson(text);
                    setupGraph();
                })
                .catch(err => {
                    console.error('Failed to load family_tree.ged:', err);
                });
        } else {
            setupGraph();
        }
    }

    function setupGraph() {
        setupD3Zoom();
        setupEventListeners();

        // Find Emil Kerimov as default home individual
        const emil = parsedGedcomJson.indis.find(i =>
            (i.id === 'I6000000003244652287' || i.id === 'I6000000003244433950') ||
            (i.firstName === 'Emil' && i.lastName === 'Kerimov')
        );
        defaultHomeIndi = emil ? emil.id : parsedGedcomJson.indis[0].id;

        // Read query params
        const params = new URLSearchParams(window.location.search);
        const indiParam = params.get('indi');
        const viewParam = params.get('view');

        if (viewParam && CHART_MAP[viewParam]) {
            currentView = viewParam;
            const viewSelect = document.getElementById('viewSelect');
            if (viewSelect) viewSelect.value = viewParam;
        }

        if (indiParam && isValidIndi(indiParam)) {
            currentIndi = indiParam;
        } else {
            currentIndi = defaultHomeIndi;
        }

        updatePersonSearchDisplay(currentIndi);
        renderTree(currentIndi, currentView, currentColor);
    }

    function isValidIndi(id) {
        if (!parsedGedcomJson || !parsedGedcomJson.indis) return false;
        return parsedGedcomJson.indis.some(i => i.id === id);
    }

    function setupD3Zoom() {
        svgSelection = Topola.d3.select('#graph-svg');
        zoomLayer = Topola.d3.select('#zoom-layer');
        const container = document.getElementById('graph-container');

        zoomBehavior = Topola.d3.zoom()
            .scaleExtent([0.05, 3.5])
            .wheelDelta(function (event) {
                // Smooth, comfortable scroll wheel delta
                return -event.deltaY * (event.deltaMode === 1 ? 0.05 : event.deltaMode ? 1 : 0.0018);
            })
            .on('start', function () {
                if (container) container.classList.add('is-panning');
            })
            .on('zoom', function (event) {
                zoomLayer.attr('transform', event.transform);
                hidePopover();
            })
            .on('end', function () {
                if (container) container.classList.remove('is-panning');
            });

        svgSelection.call(zoomBehavior);

        // Disable D3's default double-click zoom to allow double-click person centering
        svgSelection.on('dblclick.zoom', null);

        // Double-click interaction: center on clicked node or center on current person if clicking empty canvas
        svgSelection.on('dblclick', function (event) {
            const nodeEl = event.target.closest('.node');
            if (nodeEl && nodeEl.__data__) {
                const d = nodeEl.__data__;
                const targetIndi = (d.data && d.data.indi) ? d.data.indi.id : d.id;
                if (targetIndi && isValidIndi(targetIndi)) {
                    currentIndi = targetIndi;
                    updatePersonSearchDisplay(currentIndi);
                    renderTree(currentIndi, currentView, currentColor);
                    hidePopover();
                }
            } else {
                centerOnPerson(currentIndi, 0.9, true);
            }
        });
    }

    function setupEventListeners() {
        const container = document.getElementById('graph-container');
        if (container) {
            container.addEventListener('click', function (e) {
                const rect = container.getBoundingClientRect();
                lastClickPos = {
                    x: e.clientX - rect.left,
                    y: e.clientY - rect.top
                };
            }, true);
        }

        // View selection
        const viewSelect = document.getElementById('viewSelect');
        if (viewSelect) {
            viewSelect.addEventListener('change', function () {
                currentView = this.value;
                renderTree(currentIndi, currentView, currentColor);
            });
        }

        // Color selection
        const colorSelect = document.getElementById('colorSelect');
        if (colorSelect) {
            colorSelect.addEventListener('change', function () {
                currentColor = this.value;
                renderTree(currentIndi, currentView, currentColor);
            });
        }

        // Person search input & clear button
        const personInput = document.getElementById('personSearch');
        const clearBtn = document.getElementById('clearSearchBtn');

        if (personInput) {
            personInput.addEventListener('input', function () {
                if (clearBtn) {
                    clearBtn.style.display = this.value ? 'block' : 'none';
                }
            });

            personInput.addEventListener('change', handlePersonSearch);
            personInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') handlePersonSearch();
            });
            personInput.addEventListener('focus', function () {
                this.select();
            });
        }

        if (clearBtn && personInput) {
            clearBtn.addEventListener('click', function () {
                personInput.value = '';
                clearBtn.style.display = 'none';
                personInput.focus();
            });
        }

        // Home / Reset to Emil button
        const homeBtn = document.getElementById('homeBtn');
        if (homeBtn) {
            homeBtn.addEventListener('click', function () {
                if (defaultHomeIndi) {
                    if (currentIndi !== defaultHomeIndi) {
                        currentIndi = defaultHomeIndi;
                        updatePersonSearchDisplay(currentIndi);
                        renderTree(currentIndi, currentView, currentColor);
                    } else {
                        centerOnPerson(defaultHomeIndi, 0.9, true);
                    }
                }
            });
        }

        // Fit Entire Tree button
        const fitViewBtn = document.getElementById('fitViewBtn');
        if (fitViewBtn) {
            fitViewBtn.addEventListener('click', function () {
                fitToScreen(true);
            });
        }

        // Popover buttons
        const popoverClose = document.getElementById('popover-close');
        if (popoverClose) {
            popoverClose.addEventListener('click', hidePopover);
        }

        const centerBtn = document.getElementById('popover-center-btn');
        if (centerBtn) {
            centerBtn.addEventListener('click', function () {
                if (selectedIndiId && isValidIndi(selectedIndiId)) {
                    currentIndi = selectedIndiId;
                    updatePersonSearchDisplay(currentIndi);
                    renderTree(currentIndi, currentView, currentColor);
                    hidePopover();
                }
            });
        }

        // Dismiss popover on outside click or Escape key
        document.addEventListener('click', function (e) {
            const popover = document.getElementById('person-popover');
            if (popover && popover.style.display !== 'none') {
                if (!popover.contains(e.target) && !e.target.closest('.node')) {
                    hidePopover();
                }
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') hidePopover();
        });
    }

    function handlePersonSearch() {
        const input = document.getElementById('personSearch');
        if (!input) return;
        const val = input.value.trim();
        if (!val) return;

        const match = val.match(/\[([^\]]+)\]$/);
        const targetId = match ? match[1] : (familyGraph[val] ? val : null);

        if (targetId && isValidIndi(targetId)) {
            currentIndi = targetId;
            updatePersonSearchDisplay(currentIndi);
            renderTree(currentIndi, currentView, currentColor);
        } else {
            const lower = val.toLowerCase();
            const found = parsedGedcomJson.indis.find(i => {
                const full = ((i.firstName || '') + ' ' + (i.lastName || '')).toLowerCase();
                return full === lower || full.includes(lower);
            });
            if (found) {
                currentIndi = found.id;
                updatePersonSearchDisplay(currentIndi);
                renderTree(currentIndi, currentView, currentColor);
            }
        }
    }

    function updatePersonSearchDisplay(indiId) {
        const input = document.getElementById('personSearch');
        const clearBtn = document.getElementById('clearSearchBtn');
        if (!input) return;

        const p = familyGraph[indiId];
        if (p) {
            let dates = '';
            if (p.birth || p.death) {
                const b = p.birth ? '*' + p.birth : '';
                const d = p.death ? '+' + p.death : '';
                dates = ` (${[b, d].filter(Boolean).join(' ')})`;
            }
            input.value = `${p.name}${dates} [${p.id}]`;
        } else {
            const indi = parsedGedcomJson.indis.find(i => i.id === indiId);
            if (indi) {
                const name = [indi.firstName, indi.lastName].filter(Boolean).join(' ') || indiId;
                input.value = `${name} [${indiId}]`;
            } else {
                input.value = indiId;
            }
        }

        if (clearBtn) {
            clearBtn.style.display = input.value ? 'block' : 'none';
        }
    }

    function renderTree(startIndi, viewType, colorMode) {
        const treeContainer = document.getElementById('tree-container');
        if (!treeContainer) return;
        treeContainer.innerHTML = '';

        const ChartClass = CHART_MAP[viewType] || Topola.RelativesChart;
        const colors = COLOR_MAP[colorMode] !== undefined ? COLOR_MAP[colorMode] : Topola.ChartColors.BY_SEX;

        try {
            const chartHandle = Topola.createChart({
                json: parsedGedcomJson,
                chartType: ChartClass,
                renderer: Topola.DetailedRenderer,
                svgSelector: '#tree-container',
                colors: colors,
                animate: false,
                updateSvgSize: false,
                expanders: true,
                indiCallback: function (info) {
                    handleIndiClick(info.id);
                }
            });

            const info = chartHandle.render({ startIndi: startIndi });
            lastChartInfo = info;

            // Option B: For large charts (like Relatives) or whenever fit scale would be tiny (< 0.65),
            // auto-center directly onto the focal individual at a crisp, comfortable zoom scale (0.9x).
            const svgNode = document.getElementById('graph-svg');
            const containerWidth = svgNode.clientWidth || 800;
            const containerHeight = svgNode.clientHeight || 600;
            const scaleX = (containerWidth - 60) / (info.size[0] || 1000);
            const scaleY = (containerHeight - 60) / (info.size[1] || 800);
            const fitScale = Math.min(scaleX, scaleY);

            if (viewType === 'relatives' || fitScale < 0.65) {
                centerOnPerson(startIndi, 0.9, false);
            } else {
                fitToScreen(false);
            }

            updateUrl(startIndi, viewType);
        } catch (err) {
            console.error('Error rendering chart with Topola:', err);
        }
    }

    function centerOnPerson(indiId, targetScale = 0.9, animate = true) {
        const svgNode = document.getElementById('graph-svg');
        if (!svgNode) return;

        // Locate node element for indiId
        const nodes = document.querySelectorAll('#tree-container .node');
        let focalNode = null;
        for (const n of nodes) {
            const d = n.__data__;
            if (d && ((d.data && d.data.indi && d.data.indi.id === indiId) || d.id === indiId)) {
                focalNode = n;
                break;
            }
        }
        if (!focalNode) {
            focalNode = document.querySelector('#tree-container .node.generation0') || document.querySelector('#tree-container .node');
        }
        if (!focalNode) return;

        const svgWidth = svgNode.clientWidth || 800;
        const svgHeight = svgNode.clientHeight || 600;

        const innerG = document.querySelector('#tree-container > g');
        const transformStr = innerG ? innerG.getAttribute('transform') : '';
        const match = transformStr ? transformStr.match(/translate\(([^,\s]+)[,\s]+([^)]+)\)/) : null;
        const originX = match ? parseFloat(match[1]) : (lastChartInfo ? lastChartInfo.origin[0] : 0);
        const originY = match ? parseFloat(match[2]) : (lastChartInfo ? lastChartInfo.origin[1] : 0);

        const d = focalNode.__data__;
        const focalX = originX + (d ? d.x : 0);
        const focalY = originY + (d ? d.y : 0);

        const k = targetScale || 0.9;
        const tx = (svgWidth / 2) - k * focalX;
        const ty = (svgHeight / 2) - k * focalY;

        const transform = Topola.d3.zoomIdentity.translate(tx, ty).scale(k);

        if (animate) {
            svgSelection.transition().duration(500).call(zoomBehavior.transform, transform);
        } else {
            svgSelection.call(zoomBehavior.transform, transform);
        }
    }

    function fitToScreen(animate = true) {
        const info = lastChartInfo;
        const svgNode = document.getElementById('graph-svg');
        if (!info || !info.size || !svgNode) return;

        const containerWidth = svgNode.clientWidth || 800;
        const containerHeight = svgNode.clientHeight || 600;
        const chartWidth = info.size[0] || 1000;
        const chartHeight = info.size[1] || 800;
        const padding = 60;

        const scaleX = (containerWidth - padding) / chartWidth;
        const scaleY = (containerHeight - padding) / chartHeight;
        let scale = Math.min(scaleX, scaleY, 1.15);
        if (scale < 0.05) scale = 0.05;

        const tx = (containerWidth - chartWidth * scale) / 2;
        const ty = (containerHeight - chartHeight * scale) / 2;

        const transform = Topola.d3.zoomIdentity.translate(tx, ty).scale(scale);

        if (animate) {
            svgSelection.transition().duration(500).call(zoomBehavior.transform, transform);
        } else {
            svgSelection.call(zoomBehavior.transform, transform);
        }
    }

    function handleIndiClick(indiId) {
        const now = Date.now();
        if (lastClickedIndi === indiId && (now - lastClickTime) < 380) {
            // Double-click detected: re-center immediately on this individual
            hidePopover();
            currentIndi = indiId;
            updatePersonSearchDisplay(currentIndi);
            renderTree(currentIndi, currentView, currentColor);
            lastClickedIndi = null;
            lastClickTime = 0;
            return;
        }
        lastClickedIndi = indiId;
        lastClickTime = now;
        showPopover(indiId);
    }

    function showPopover(indiId) {
        selectedIndiId = indiId;
        const p = familyGraph[indiId];
        let name = indiId;
        let dates = '';
        let path = '';

        if (p) {
            name = p.name || indiId;
            const b = p.birth ? 'b. ' + p.birth : '';
            const d = p.death ? 'd. ' + p.death : '';
            dates = [b, d].filter(Boolean).join('  |  ');
            path = p.path || '';
        } else {
            const indi = parsedGedcomJson.indis.find(x => x.id === indiId);
            if (indi) {
                name = [indi.firstName, indi.lastName].filter(Boolean).join(' ') || indiId;
                const b = (indi.birth && indi.birth.date) ? 'b. ' + indi.birth.date.year : '';
                const d = (indi.death && indi.death.date) ? 'd. ' + indi.death.date.year : '';
                dates = [b, d].filter(Boolean).join('  |  ');
            }
        }

        const nameEl = document.getElementById('popover-name');
        const datesEl = document.getElementById('popover-dates');
        const viewBtn = document.getElementById('popover-view-btn');
        const relBtn = document.getElementById('popover-rel-btn');
        const popover = document.getElementById('person-popover');
        const container = document.getElementById('graph-container');

        if (nameEl) nameEl.textContent = name;
        if (datesEl) datesEl.textContent = dates ? `${dates}  [${indiId}]` : `[${indiId}]`;

        if (viewBtn) {
            if (path) {
                viewBtn.href = path;
                viewBtn.style.display = 'block';
            } else {
                viewBtn.style.display = 'none';
            }
        }

        if (relBtn) {
            relBtn.href = 'relationship.html?p1=' + encodeURIComponent(indiId);
        }

        if (popover && container) {
            const maxW = container.clientWidth;
            const maxH = container.clientHeight;

            let posX = lastClickPos.x + 12;
            let posY = lastClickPos.y + 12;

            if (posX + 260 > maxW) posX = maxW - 270;
            if (posY + 170 > maxH) posY = maxH - 180;
            if (posX < 10) posX = 10;
            if (posY < 10) posY = 10;

            popover.style.left = posX + 'px';
            popover.style.top = posY + 'px';
            popover.style.display = 'block';
        }
    }

    function hidePopover() {
        const popover = document.getElementById('person-popover');
        if (popover) {
            popover.style.display = 'none';
        }
    }

    function updateUrl(indi, view) {
        try {
            const url = new URL(window.location);
            url.searchParams.set('indi', indi);
            url.searchParams.set('view', view);
            window.history.replaceState({}, '', url);
        } catch (e) {
            // Ignore in restricted environments
        }
    }

    window.addEventListener('DOMContentLoaded', init);
})();

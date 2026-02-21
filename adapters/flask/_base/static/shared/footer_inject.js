/**
 * Tool Hub Footer Injector
 * Add this script to any tool template to automatically include the shared footer
 *
 * Usage: <script src="/shared/footer.js"></script>
 */

(function() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectFooter);
    } else {
        injectFooter();
    }

    function injectFooter() {
        // Fetch and inject the shared footer HTML
        fetch('/shared/footer')
            .then(response => response.text())
            .then(html => {
                // Create a container and inject the footer
                const container = document.createElement('div');
                container.innerHTML = html;
                document.body.appendChild(container);

                // Now run the footer logic (inline scripts don't execute via innerHTML)
                loadToolsIntoFooter();
                adjustBodyForFooter();
            })
            .catch(err => {
                console.error('Failed to load Tool Hub footer:', err);
            });
    }

    function loadToolsIntoFooter() {
        // Fetch tools list from hub API
        fetch('/api/tools')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch tools: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                const toolsList = document.getElementById('toolsList');
                const toolCount = document.getElementById('toolCount');
                const currentPath = window.location.pathname;

                if (!toolsList || !toolCount) {
                    console.error('Footer elements not found');
                    return;
                }

                // Update count
                toolCount.textContent = data.tools.length + ' tools';

                // Clear loading text
                toolsList.innerHTML = '';

                // Generate tool links
                data.tools.forEach(tool => {
                    const link = document.createElement('a');
                    link.href = tool.path;
                    link.className = 'tool-hub-footer-tool';

                    // Mark active tool
                    if (currentPath.startsWith(tool.path.replace(/\/$/, ''))) {
                        link.classList.add('active');
                    }

                    link.innerHTML = '<span class="footer-icon"><i data-lucide="' + tool.icon + '"></i></span><span>' + tool.name + '</span>';
                    toolsList.appendChild(link);
                });

                if (window.lucide) {
                    window.lucide.createIcons();
                }
            })
            .catch(err => {
                console.error('Failed to load tools:', err);
                // Fallback: show hardcoded tools
                const toolsList = document.getElementById('toolsList');
                const toolCount = document.getElementById('toolCount');

                if (toolCount) toolCount.textContent = '2 tools';
                if (toolsList) {
                    toolsList.innerHTML = '';

                    // Hardcoded fallback
                    const tools = [
                        { icon: 'tags', name: 'Labels', path: '/labels/' },
                        { icon: 'file-text', name: 'PDF Splitter', path: '/pdf/' }
                    ];

                    tools.forEach(tool => {
                        const link = document.createElement('a');
                        link.href = tool.path;
                        link.className = 'tool-hub-footer-tool';
                        link.innerHTML = '<span class="footer-icon"><i data-lucide="' + tool.icon + '"></i></span><span>' + tool.name + '</span>';
                        toolsList.appendChild(link);
                    });
                }
            });
    }

    function adjustBodyForFooter() {
        const footer = document.getElementById('toolHubFooter');
        if (!footer) return;

        const applyPadding = () => {
            const height = footer.offsetHeight || 0;
            document.body.style.paddingBottom = `${height + 20}px`;
        };

        applyPadding();
        window.addEventListener('resize', applyPadding);
    }
})();

// Docs as Code - Interactive Systems Thinking Components
// Based on Donella H. Meadows' "Thinking in Systems" methodology

class DocsAsCodeSystem {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupSmoothScrolling();
        this.setupSystemCards();
        this.setupModals();
    }

    init() {
        // Initialize the system
        console.log('Docs as Code System initialized');
        this.currentModal = null;
        this.systemCards = document.querySelectorAll('.system-card');
        this.setupWorkflowTabs();
    }

    setupEventListeners() {
        // Navigation smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = anchor.getAttribute('href').substring(1);
                this.scrollToSection(targetId);
            });
        });

        // System card interactions
        this.systemCards.forEach(card => {
            card.addEventListener('click', () => {
                this.highlightSystemLevel(card);
            });

            card.addEventListener('mouseenter', () => {
                this.showSystemConnections(card);
            });

            card.addEventListener('mouseleave', () => {
                this.hideSystemConnections();
            });
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentModal) {
                this.closeModal();
            }
        });

        // Window resize handling
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    setupSmoothScrolling() {
        // Smooth scrolling with easing
        this.scrollToSection = (sectionId) => {
            const target = document.getElementById(sectionId);
            if (target) {
                const headerHeight = document.querySelector('.nav').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        };
    }

    setupSystemCards() {
        // Add interactive features to system cards
        this.systemCards.forEach((card, index) => {
            const level = card.dataset.level;
            
            // Add level-specific styling
            card.style.setProperty('--card-delay', `${index * 100}ms`);
            
            // Add animation on scroll
            this.observeCard(card);
        });
    }

    observeCard(card) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationDelay = entry.target.style.getPropertyValue('--card-delay');
                    entry.target.classList.add('animate-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        observer.observe(card);
    }

    highlightSystemLevel(card) {
        // Remove previous highlights
        this.systemCards.forEach(c => c.classList.remove('highlighted'));
        
        // Highlight clicked card
        card.classList.add('highlighted');
        
        // Show related information
        const level = card.dataset.level;
        this.showLevelDetails(level);
    }

    showSystemConnections(card) {
        const level = parseInt(card.dataset.level);
        
        // Highlight connected levels (adjacent levels in Meadows' framework)
        this.systemCards.forEach(c => {
            const cardLevel = parseInt(c.dataset.level);
            if (Math.abs(cardLevel - level) === 1) {
                c.classList.add('connected');
            }
        });
    }

    hideSystemConnections() {
        this.systemCards.forEach(c => {
            c.classList.remove('connected');
        });
    }

    showLevelDetails(level) {
        const details = this.getLevelDetails(level);
        
        // Create or update details panel
        let detailsPanel = document.getElementById('level-details');
        if (!detailsPanel) {
            detailsPanel = document.createElement('div');
            detailsPanel.id = 'level-details';
            detailsPanel.className = 'level-details-panel';
            document.body.appendChild(detailsPanel);
        }
        
        detailsPanel.innerHTML = `
            <div class="details-content">
                <h3>Level ${level}: ${details.title}</h3>
                <p>${details.description}</p>
                <div class="details-examples">
                    ${details.examples.map(example => `
                        <div class="example-item">
                            <strong>${example.title}:</strong> ${example.description}
                        </div>
                    `).join('')}
                </div>
                <button class="btn btn-outline" onclick="this.parentElement.parentElement.remove()">
                    Close
                </button>
            </div>
        `;
        
        // Animate in
        setTimeout(() => {
            detailsPanel.classList.add('show');
        }, 10);
    }

    getLevelDetails(level) {
        const levelData = {
            12: {
                title: 'Paradigms',
                description: 'The deepest level of change - fundamental beliefs and assumptions about how documentation should work.',
                examples: [
                    {
                        title: 'Old Paradigm',
                        description: 'Documentation is an afterthought, created separately from development'
                    },
                    {
                        title: 'New Paradigm',
                        description: 'Documentation is a first-class citizen, integrated into the development process'
                    }
                ]
            },
            11: {
                title: 'Goals',
                description: 'The purpose and objectives that drive the documentation system.',
                examples: [
                    {
                        title: 'Primary Goal',
                        description: 'Create maintainable, collaborative, and automated documentation'
                    },
                    {
                        title: 'Supporting Goals',
                        description: 'Version control, automated testing, continuous integration'
                    }
                ]
            },
            10: {
                title: 'Self-Organization',
                description: 'How the system evolves and adapts without external control.',
                examples: [
                    {
                        title: 'Community Contribution',
                        description: 'Documentation improves through collaborative input'
                    },
                    {
                        title: 'Emergent Behavior',
                        description: 'New patterns emerge from collective action'
                    }
                ]
            },
            9: {
                title: 'System Rules',
                description: 'Governance policies and constraints that shape behavior.',
                examples: [
                    {
                        title: 'Pull Request Policy',
                        description: 'All changes require peer review'
                    },
                    {
                        title: 'Format Standards',
                        description: 'Plain text formats only for portability'
                    }
                ]
            },
            8: {
                title: 'Information Flows',
                description: 'How information moves through the system.',
                examples: [
                    {
                        title: 'Code to Docs',
                        description: 'Changes in code trigger documentation updates'
                    },
                    {
                        title: 'Feedback Loop',
                        description: 'User feedback informs documentation improvements'
                    }
                ]
            },
            7: {
                title: 'Feedback Loops',
                description: 'Reinforcing and balancing mechanisms that drive system behavior.',
                examples: [
                    {
                        title: 'Reinforcing Loop',
                        description: 'Better docs attract more contributors'
                    },
                    {
                        title: 'Balancing Loop',
                        description: 'Complexity drives automation efforts'
                    }
                ]
            },
            6: {
                title: 'Structure',
                description: 'Physical and organizational arrangement of system components.',
                examples: [
                    {
                        title: 'Repository Structure',
                        description: 'Organized file hierarchy and naming conventions'
                    },
                    {
                        title: 'Build Pipeline',
                        description: 'Automated processes for testing and deployment'
                    }
                ]
            },
            5: {
                title: 'Delays',
                description: 'Time lags in system responses and processes.',
                examples: [
                    {
                        title: 'Review Process',
                        description: 'Time between submission and approval'
                    },
                    {
                        title: 'Learning Curve',
                        description: 'Time for new contributors to become productive'
                    }
                ]
            },
            4: {
                title: 'Stocks & Flows',
                description: 'What accumulates in the system and what flows through it.',
                examples: [
                    {
                        title: 'Stocks',
                        description: 'Documentation content, community knowledge, tool expertise'
                    },
                    {
                        title: 'Flows',
                        description: 'Content creation rate, review throughput, deployment frequency'
                    }
                ]
            },
            3: {
                title: 'Driving Forces',
                description: 'External influences that shape system behavior.',
                examples: [
                    {
                        title: 'Positive Forces',
                        description: 'Developer productivity needs, quality standards'
                    },
                    {
                        title: 'Negative Forces',
                        description: 'Technical complexity, resource constraints'
                    }
                ]
            },
            2: {
                title: 'System Behavior',
                description: 'Observable patterns and trends over time.',
                examples: [
                    {
                        title: 'Growth Pattern',
                        description: 'Exponential growth in contributors'
                    },
                    {
                        title: 'Cyclical Pattern',
                        description: 'Regular review and update cycles'
                    }
                ]
            },
            1: {
                title: 'Events',
                description: 'Specific incidents and observable occurrences.',
                examples: [
                    {
                        title: 'Pull Request',
                        description: 'Documentation change submitted for review'
                    },
                    {
                        title: 'Deployment',
                        description: 'Updated documentation goes live'
                    }
                ]
            }
        };
        
        return levelData[level] || { title: 'Unknown', description: 'No details available', examples: [] };
    }

    setupModals() {
        // Modal functionality
        this.modalFunctions = {
            assessment: () => this.toggleModal('assessment-modal'),
            paradigm: () => this.toggleModal('paradigm-modal'),
            rules: () => this.toggleModal('rules-modal'),
            flows: () => this.toggleModal('flows-modal'),
            tools: () => this.toggleModal('tools-modal'),
            monitoring: () => this.toggleModal('monitoring-modal')
        };
    }

    setupWorkflowTabs() {
        // Workflow tab functionality
        this.workflowTabs = document.querySelectorAll('.tab-btn');
        this.workflowContents = document.querySelectorAll('.workflow-content');
        
        this.workflowTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.textContent.toLowerCase().replace(/\s+/g, '-');
                this.showWorkflow(targetId);
            });
        });
    }

    toggleModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) {
            this.createModal(modalId);
            return;
        }
        
        if (modal.style.display === 'block') {
            this.closeModal();
        } else {
            this.openModal(modal);
        }
    }

    createModal(modalId) {
        const modalContent = this.getModalContent(modalId);
        if (!modalContent) return;
        
        const modal = document.createElement('div');
        modal.id = modalId;
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close" onclick="docsAsCodeSystem.closeModal()">&times;</span>
                ${modalContent}
            </div>
        `;
        
        document.body.appendChild(modal);
        this.openModal(modal);
    }

    getModalContent(modalId) {
        const content = {
            'assessment-modal': `
                <h2>System Assessment Checklist</h2>
                <div class="checklist">
                    <div class="checklist-item">
                        <input type="checkbox" id="current-docs">
                        <label for="current-docs">Map current documentation structure and workflows</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="stakeholders">
                        <label for="stakeholders">Identify all stakeholders (developers, writers, users)</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="pain-points">
                        <label for="pain-points">Document pain points and bottlenecks in current system</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="tools-audit">
                        <label for="tools-audit">Audit current tools and their limitations</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="feedback-loops">
                        <label for="feedback-loops">Analyze existing feedback loops and information flows</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="goals-alignment">
                        <label for="goals-alignment">Assess alignment between stated and actual goals</label>
                    </div>
                </div>
            `,
            'paradigm-modal': `
                <h2>Paradigm Shift Guide</h2>
                <div class="paradigm-shift-content">
                    <div class="shift-step">
                        <h3>1. Recognize Current Paradigm</h3>
                        <p>Documentation is often treated as a separate, secondary activity that happens after development.</p>
                    </div>
                    <div class="shift-step">
                        <h3>2. Identify Limitations</h3>
                        <p>This paradigm leads to outdated content, poor collaboration, and maintenance overhead.</p>
                    </div>
                    <div class="shift-step">
                        <h3>3. Envision New Paradigm</h3>
                        <p>Documentation as a first-class citizen, integrated into development workflows.</p>
                    </div>
                    <div class="shift-step">
                        <h3>4. Create Supporting Structures</h3>
                        <p>Implement tools, processes, and cultural changes that support the new paradigm.</p>
                    </div>
                </div>
            `,
            'rules-modal': `
                <h2>Policy Templates</h2>
                <div class="policy-templates">
                    <div class="policy-template">
                        <h3>Contribution Guidelines</h3>
                        <ul>
                            <li>All documentation changes require pull requests</li>
                            <li>Minimum two reviewers for significant changes</li>
                            <li>Automated testing must pass before merge</li>
                            <li>Follow established style guides</li>
                        </ul>
                    </div>
                    <div class="policy-template">
                        <h3>Content Standards</h3>
                        <ul>
                            <li>Use plain text formats (Markdown, reStructuredText)</li>
                            <li>Include code examples for all APIs</li>
                            <li>Maintain consistent terminology</li>
                            <li>Regular review cycles for accuracy</li>
                        </ul>
                    </div>
                    <div class="policy-template">
                        <h3>Quality Assurance</h3>
                        <ul>
                            <li>Automated link checking</li>
                            <li>Style and grammar validation</li>
                            <li>Accessibility compliance</li>
                            <li>Performance monitoring</li>
                        </ul>
                    </div>
                </div>
            `,
            'flows-modal': `
                <h2>Information Flow Diagrams</h2>
                <div class="flow-diagrams">
                    <div class="flow-diagram">
                        <h3>Development to Documentation Flow</h3>
                        <div class="flow-visual">
                            <div class="flow-node">Code Change</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">API Update</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Doc Update</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Review</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Deploy</div>
                        </div>
                    </div>
                    <div class="flow-diagram">
                        <h3>User Feedback Loop</h3>
                        <div class="flow-visual">
                            <div class="flow-node">User Issue</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Feedback</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Improvement</div>
                            <div class="flow-arrow">→</div>
                            <div class="flow-node">Updated Docs</div>
                        </div>
                    </div>
                </div>
            `,
            'tools-modal': `
                <h2>Tool Selection Guide</h2>
                <div class="tool-categories">
                    <div class="tool-category">
                        <h3>Static Site Generators</h3>
                        <div class="tool-options">
                            <div class="tool-option">
                                <strong>Hugo</strong> - Fast, single binary, great for large sites
                            </div>
                            <div class="tool-option">
                                <strong>MkDocs</strong> - Simple, Python-based, good for projects
                            </div>
                            <div class="tool-option">
                                <strong>Sphinx</strong> - Powerful, Python ecosystem, API docs
                            </div>
                            <div class="tool-option">
                                <strong>Jekyll</strong> - GitHub Pages native, Ruby-based
                            </div>
                        </div>
                    </div>
                    <div class="tool-category">
                        <h3>Hosting Platforms</h3>
                        <div class="tool-options">
                            <div class="tool-option">
                                <strong>GitHub Pages</strong> - Free, integrated with Git
                            </div>
                            <div class="tool-option">
                                <strong>Netlify</strong> - Advanced features, form handling
                            </div>
                            <div class="tool-option">
                                <strong>Vercel</strong> - Fast, global CDN, previews
                            </div>
                            <div class="tool-option">
                                <strong>Read the Docs</strong> - Specialized for documentation
                            </div>
                        </div>
                    </div>
                </div>
            `,
            'monitoring-modal': `
                <h2>Monitoring Framework</h2>
                <div class="monitoring-framework">
                    <div class="monitoring-category">
                        <h3>Content Quality Metrics</h3>
                        <ul>
                            <li>Broken link count</li>
                            <li>Outdated content percentage</li>
                            <li>Review cycle time</li>
                            <li>Contributor engagement</li>
                        </ul>
                    </div>
                    <div class="monitoring-category">
                        <h3>User Experience Metrics</h3>
                        <ul>
                            <li>Page load times</li>
                            <li>Search success rate</li>
                            <li>User feedback scores</li>
                            <li>Support ticket reduction</li>
                        </ul>
                    </div>
                    <div class="monitoring-category">
                        <h3>System Health Metrics</h3>
                        <ul>
                            <li>Build success rate</li>
                            <li>Deployment frequency</li>
                            <li>Tool uptime</li>
                            <li>Security compliance</li>
                        </ul>
                    </div>
                </div>
            `
        };
        
        return content[modalId];
    }

    openModal(modal) {
        modal.style.display = 'block';
        this.currentModal = modal;
        document.body.style.overflow = 'hidden';
        
        // Animate in
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
    }

    closeModal() {
        if (this.currentModal) {
            this.currentModal.classList.remove('show');
            setTimeout(() => {
                this.currentModal.style.display = 'none';
                this.currentModal = null;
                document.body.style.overflow = 'auto';
            }, 300);
        }
    }

    handleResize() {
        // Handle responsive adjustments
        const isMobile = window.innerWidth < 768;
        
        // Adjust system card interactions for mobile
        this.systemCards.forEach(card => {
            if (isMobile) {
                card.style.cursor = 'pointer';
            } else {
                card.style.cursor = 'default';
            }
        });
    }
}

// Global functions for HTML onclick handlers
function scrollToSection(sectionId) {
    docsAsCodeSystem.scrollToSection(sectionId);
}

function showWorkflow(workflowId) {
    // Remove active class from all tabs and contents
    document.querySelectorAll('.tab-btn').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.workflow-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    const targetTab = Array.from(document.querySelectorAll('.tab-btn')).find(tab => 
        tab.textContent.toLowerCase().replace(/\s+/g, '-') === workflowId
    );
    const targetContent = document.getElementById(workflowId);
    
    if (targetTab) targetTab.classList.add('active');
    if (targetContent) targetContent.classList.add('active');
}

function showAIWorkflow(workflowId) {
    // Remove active class from all AI workflow tabs and contents
    document.querySelectorAll('.ai-workflow-tabs .tab-btn').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.ai-workflow-tabs .workflow-content').forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and content
    const targetTab = Array.from(document.querySelectorAll('.ai-workflow-tabs .tab-btn')).find(tab => 
        tab.textContent.toLowerCase().replace(/\s+/g, '-') === workflowId
    );
    const targetContent = document.getElementById(workflowId);
    
    if (targetTab) targetTab.classList.add('active');
    if (targetContent) targetContent.classList.add('active');
}

function showAIDemo(demoType) {
    const demos = {
        'content-generation': {
            title: 'AI Content Generation Demo',
            content: `
                <div class="demo-content">
                    <h3>Generate Documentation from Code</h3>
                    <div class="demo-input">
                        <label>Paste your code here:</label>
                        <textarea placeholder="// Example API endpoint
@GET("/api/users/{id}")
public User getUser(@PathParam("id") String id) {
    return userService.findById(id);
}" rows="6"></textarea>
                    </div>
                    <button class="btn btn-primary" onclick="generateDocs()">
                        <i class="fas fa-magic"></i>
                        Generate Documentation
                    </button>
                    <div class="demo-output" id="generated-output" style="display: none;">
                        <h4>Generated Documentation:</h4>
                        <div class="generated-docs">
                            <h5>GET /api/users/{id}</h5>
                            <p>Retrieves user information by ID from the database.</p>
                            <div class="parameters">
                                <strong>Parameters:</strong>
                                <ul>
                                    <li><code>id</code> (String): The unique identifier of the user</li>
                                </ul>
                            </div>
                            <div class="response">
                                <strong>Response:</strong>
                                <pre><code>{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}</code></pre>
                            </div>
                        </div>
                    </div>
                </div>
            `
        },
        'intelligent-search': {
            title: 'Intelligent Search Demo',
            content: `
                <div class="demo-content">
                    <h3>Semantic Documentation Search</h3>
                    <div class="search-demo">
                        <div class="search-input">
                            <input type="text" placeholder="Ask: 'How do I handle errors?' or 'Show me authentication examples'" id="search-input">
                            <button class="btn btn-primary" onclick="performSearch()">
                                <i class="fas fa-search"></i>
                                Search
                            </button>
                        </div>
                        <div class="search-results" id="search-results" style="display: none;">
                            <div class="result-item">
                                <h5>Error Handling Guide</h5>
                                <p>Comprehensive guide on implementing error handling in your API...</p>
                                <span class="relevance">95% match</span>
                            </div>
                            <div class="result-item">
                                <h5>Authentication Examples</h5>
                                <p>Code examples for implementing OAuth 2.0 authentication...</p>
                                <span class="relevance">87% match</span>
                            </div>
                        </div>
                    </div>
                </div>
            `
        },
        'translation': {
            title: 'Smart Translation Demo',
            content: `
                <div class="demo-content">
                    <h3>AI-Powered Translation</h3>
                    <div class="translation-demo">
                        <div class="source-content">
                            <label>Source Documentation:</label>
                            <textarea placeholder="Enter your documentation text here..." rows="4"></textarea>
                        </div>
                        <div class="language-selector">
                            <label>Translate to:</label>
                            <select>
                                <option value="es">Spanish</option>
                                <option value="fr">French</option>
                                <option value="de">German</option>
                                <option value="ja">Japanese</option>
                                <option value="zh">Chinese</option>
                            </select>
                        </div>
                        <button class="btn btn-primary" onclick="translateContent()">
                            <i class="fas fa-language"></i>
                            Translate
                        </button>
                        <div class="translation-output" id="translation-output" style="display: none;">
                            <h4>Translated Documentation:</h4>
                            <div class="translated-content">
                                <p>Documentación traducida automáticamente con contexto técnico preservado...</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        },
        'quality-analysis': {
            title: 'Quality Analysis Demo',
            content: `
                <div class="demo-content">
                    <h3>AI Quality Analysis</h3>
                    <div class="quality-demo">
                        <div class="content-input">
                            <label>Analyze your documentation:</label>
                            <textarea placeholder="Paste your documentation content here..." rows="6"></textarea>
                        </div>
                        <button class="btn btn-primary" onclick="analyzeQuality()">
                            <i class="fas fa-chart-line"></i>
                            Analyze Quality
                        </button>
                        <div class="quality-results" id="quality-results" style="display: none;">
                            <div class="quality-metrics">
                                <div class="metric">
                                    <span class="metric-label">Clarity Score</span>
                                    <span class="metric-value">8.5/10</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Completeness</span>
                                    <span class="metric-value">7.2/10</span>
                                </div>
                                <div class="metric">
                                    <span class="metric-label">Accessibility</span>
                                    <span class="metric-value">9.1/10</span>
                                </div>
                            </div>
                            <div class="suggestions">
                                <h4>AI Suggestions:</h4>
                                <ul>
                                    <li>Consider adding more code examples</li>
                                    <li>Break down complex procedures into smaller steps</li>
                                    <li>Add troubleshooting section</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `
        }
    };
    
    const demo = demos[demoType];
    if (!demo) return;
    
    // Create modal for demo
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content ai-demo-modal">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <h2>${demo.title}</h2>
            ${demo.content}
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    // Animate in
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

// Demo functions
function generateDocs() {
    const output = document.getElementById('generated-output');
    if (output) {
        output.style.display = 'block';
        output.scrollIntoView({ behavior: 'smooth' });
    }
}

function performSearch() {
    const results = document.getElementById('search-results');
    if (results) {
        results.style.display = 'block';
        results.scrollIntoView({ behavior: 'smooth' });
    }
}

function translateContent() {
    const output = document.getElementById('translation-output');
    if (output) {
        output.style.display = 'block';
        output.scrollIntoView({ behavior: 'smooth' });
    }
}

function analyzeQuality() {
    const results = document.getElementById('quality-results');
    if (results) {
        results.style.display = 'block';
        results.scrollIntoView({ behavior: 'smooth' });
    }
}

function toggleAssessment() {
    docsAsCodeSystem.toggleModal('assessment-modal');
}

function toggleParadigm() {
    docsAsCodeSystem.toggleModal('paradigm-modal');
}

function toggleRules() {
    docsAsCodeSystem.toggleModal('rules-modal');
}

function toggleFlows() {
    docsAsCodeSystem.toggleModal('flows-modal');
}

function toggleTools() {
    docsAsCodeSystem.toggleModal('tools-modal');
}

function toggleMonitoring() {
    docsAsCodeSystem.toggleModal('monitoring-modal');
}

// Initialize the system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.docsAsCodeSystem = new DocsAsCodeSystem();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    .system-card {
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.6s ease-out;
    }
    
    .system-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .system-card.highlighted {
        transform: scale(1.05);
        box-shadow: 0 20px 40px rgba(37, 99, 235, 0.3);
        border-color: var(--primary-color);
    }
    
    .system-card.connected {
        border-color: var(--secondary-color);
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.05), rgba(37, 99, 235, 0.05));
    }
    
    .level-details-panel {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.9);
        background: white;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-xl);
        z-index: 1000;
        max-width: 600px;
        width: 90%;
        opacity: 0;
        transition: all 0.3s ease-out;
    }
    
    .level-details-panel.show {
        opacity: 1;
        transform: translate(-50%, -50%) scale(1);
    }
    
    .details-content {
        padding: var(--spacing-8);
    }
    
    .details-content h3 {
        color: var(--primary-color);
        margin-bottom: var(--spacing-4);
    }
    
    .details-examples {
        margin: var(--spacing-6) 0;
    }
    
    .example-item {
        padding: var(--spacing-3);
        background: var(--gray-50);
        border-radius: var(--radius-md);
        margin-bottom: var(--spacing-3);
    }
    
    .modal.show .modal-content {
        transform: scale(1);
        opacity: 1;
    }
    
    .modal .modal-content {
        transform: scale(0.9);
        opacity: 0;
        transition: all 0.3s ease-out;
    }
    
    .shift-step {
        margin-bottom: var(--spacing-6);
        padding: var(--spacing-4);
        background: var(--gray-50);
        border-radius: var(--radius-md);
    }
    
    .shift-step h3 {
        color: var(--primary-color);
        margin-bottom: var(--spacing-2);
    }
    
    .policy-template {
        margin-bottom: var(--spacing-6);
        padding: var(--spacing-4);
        background: var(--gray-50);
        border-radius: var(--radius-md);
    }
    
    .policy-template h3 {
        color: var(--primary-color);
        margin-bottom: var(--spacing-3);
    }
    
    .policy-template ul {
        list-style: none;
        margin: 0;
    }
    
    .policy-template li {
        padding: var(--spacing-2) 0;
        position: relative;
        padding-left: var(--spacing-6);
    }
    
    .policy-template li::before {
        content: '✓';
        color: var(--success-color);
        font-weight: bold;
        position: absolute;
        left: 0;
    }
    
    .flow-visual {
        display: flex;
        align-items: center;
        gap: var(--spacing-2);
        margin: var(--spacing-4) 0;
        flex-wrap: wrap;
    }
    
    .flow-node {
        padding: var(--spacing-3) var(--spacing-4);
        background: var(--primary-color);
        color: white;
        border-radius: var(--radius-md);
        font-size: var(--font-size-sm);
        font-weight: 500;
    }
    
    .flow-arrow {
        color: var(--primary-color);
        font-weight: bold;
        font-size: var(--font-size-lg);
    }
    
    .tool-category {
        margin-bottom: var(--spacing-6);
        padding: var(--spacing-4);
        background: var(--gray-50);
        border-radius: var(--radius-md);
    }
    
    .tool-category h3 {
        color: var(--primary-color);
        margin-bottom: var(--spacing-4);
    }
    
    .tool-option {
        padding: var(--spacing-3);
        background: white;
        border-radius: var(--radius-sm);
        margin-bottom: var(--spacing-2);
        border-left: 4px solid var(--primary-color);
    }
    
    .monitoring-category {
        margin-bottom: var(--spacing-6);
        padding: var(--spacing-4);
        background: var(--gray-50);
        border-radius: var(--radius-md);
    }
    
    .monitoring-category h3 {
        color: var(--primary-color);
        margin-bottom: var(--spacing-3);
    }
    
    .monitoring-category ul {
        list-style: none;
        margin: 0;
    }
    
    .monitoring-category li {
        padding: var(--spacing-2) 0;
        position: relative;
        padding-left: var(--spacing-6);
    }
    
    .monitoring-category li::before {
        content: '📊';
        position: absolute;
        left: 0;
    }
    
    @media (max-width: 768px) {
        .level-details-panel {
            width: 95%;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .flow-visual {
            flex-direction: column;
            align-items: stretch;
        }
        
        .flow-arrow {
            transform: rotate(90deg);
            text-align: center;
        }
    }
`;
document.head.appendChild(style);

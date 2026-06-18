def build_exact_clone_3():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfect Neumorphic Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        /* The exact warm background room */
        body {
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background-color: #E2D7C8; /* Fallback warm color */
        }

        /* 
         * THE SECRET TO NEUMORPHISM:
         * 1. Solid base color (not translucent)
         * 2. Shadow colors must be warm derivatives of the base color, NOT pure black with opacity.
         */
        :root {
            --base-color: #F3EFE6;
            --shadow-light: #FFFFFF;
            --shadow-dark: #D8CEBE; /* Warm dark tan */
            --text-main: #1D1F20;
            --text-sub: #7A7F87;
            --green: #2EA043;
            --red: #D92D20;
        }

        /* The Main Window */
        .window {
            background-color: var(--base-color);
            width: 96vw;
            max-width: 1250px;
            height: 88vh;
            max-height: 850px;
            border-radius: 36px;
            display: flex;
            position: relative;
            /* Very soft, expansive drop shadow to make it float */
            box-shadow: 
                0 40px 100px rgba(0, 0, 0, 0.15),
                inset 0 2px 4px rgba(255, 255, 255, 1);
        }

        /* Sidebar */
        .sidebar {
            width: 90px;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 32px 0;
            position: relative;
            /* Subtle engraved line for the sidebar */
            box-shadow: 1px 0 0 rgba(0,0,0,0.03), 2px 0 0 rgba(255,255,255,0.6);
        }

        /* The tiny notch indicator on the left edge */
        .sidebar-notch {
            position: absolute;
            left: 0;
            top: 118px; /* Aligned with active icon */
            width: 4px;
            height: 32px;
            background-color: #2B2F33;
            border-radius: 0 4px 4px 0;
        }

        /* The logo at the top left */
        .logo-box {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            background: linear-gradient(135deg, #5C6269, #202326);
            margin-bottom: 48px;
            position: relative;
            /* 3D button effect */
            box-shadow: 0 8px 16px rgba(0,0,0,0.15), inset 0 2px 4px rgba(255,255,255,0.2);
        }
        .logo-box::after {
            content: '';
            position: absolute;
            top: 0; right: 0; bottom: 0; left: 0;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 50%);
        }

        /* Sidebar Icons */
        .nav-item {
            width: 46px;
            height: 46px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            border-radius: 14px;
            cursor: pointer;
            color: #A0A5AE;
            transition: 0.2s ease;
        }
        .nav-item.active {
            background-color: #2D3135;
            color: #FFFFFF;
            /* Inward bevel and drop shadow for the dark button */
            box-shadow: 
                0 10px 20px rgba(0, 0, 0, 0.15),
                inset 0 1px 1px rgba(255, 255, 255, 0.1);
        }
        .nav-item svg { width: 22px; height: 22px; stroke-width: 2.2; }

        /* Main Workspace Area */
        .workspace {
            flex: 1;
            padding: 32px 48px 40px 48px;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 36px;
        }
        .header h1 {
            font-size: 26px;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.5px;
        }
        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .date {
            font-size: 14px;
            font-weight: 500;
            color: var(--text-sub);
        }
        .lang-pill {
            background-color: #F8F5EF;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
            /* A slightly raised pill */
            box-shadow: 
                -4px -4px 10px #FFFFFF,
                4px 4px 10px var(--shadow-dark);
            cursor: pointer;
        }

        /* Neumorphic Grid */
        .grid {
            display: grid;
            grid-template-columns: 1.1fr 1fr 1fr;
            gap: 28px; /* The spaces between the bubbles */
        }

        /* The Bubble Cards */
        .card {
            background-color: var(--base-color);
            border-radius: 32px; /* Very rounded Squircles */
            padding: 30px;
            /* The perfect neumorphic 3D shadow */
            box-shadow: 
                -12px -12px 30px var(--shadow-light),
                12px 12px 30px var(--shadow-dark);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .card-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-main);
        }
        .more-dots {
            color: #A0A5AE;
            cursor: pointer;
        }

        /* Text Utilities */
        .label {
            font-size: 13px;
            font-weight: 500;
            color: var(--text-sub);
            margin-bottom: 4px;
        }
        .big-number {
            font-size: 32px;
            font-weight: 800;
            color: var(--text-main);
            letter-spacing: -1px;
            line-height: 1.1;
        }
        .indicator {
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .indicator svg { width: 12px; height: 12px; stroke-width: 3; }
        .green { color: var(--green); }
        .red { color: var(--red); }
        
        .metric-group {
            margin-bottom: 24px;
        }
        .metric-value-row {
            display: flex;
            align-items: flex-end;
            gap: 12px;
        }

        /* Progress Bar (Pulse) */
        .progress-bar-container {
            margin: 10px 0;
        }
        .pulse-text {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 8px;
        }
        .segments {
            display: flex;
            gap: 6px;
        }
        .segment {
            height: 8px;
            border-radius: 4px;
            background-color: #6C737E; /* Solid dark gray */
            flex: 1;
        }
        .segment.half {
            background: linear-gradient(90deg, #6C737E 50%, #D8D2C5 50%);
        }
        .segment.empty {
            background-color: #D8D2C5;
        }
        .segment-labels {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 600;
            color: #A0A5AE;
            margin-top: 6px;
        }

        /* Recent Activity List */
        .activity-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }
        .activity-row:last-child { margin-bottom: 0; }
        .act-title { font-size: 13px; color: var(--text-sub); margin-bottom: 2px; }
        .act-name { font-size: 15px; font-weight: 600; color: var(--text-main); }
        .act-time { font-size: 12px; color: var(--text-sub); margin-top: 2px; }

        /* Team Overview */
        .team-row {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
        }
        .team-row:last-child { margin-bottom: 0; }
        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: var(--base-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-main);
            /* Inner shadow to make it look indented */
            box-shadow: 
                inset 3px 3px 6px var(--shadow-dark),
                inset -3px -3px 6px var(--shadow-light);
        }

        /* Placements */
        .p-summary { grid-column: 1; grid-row: 1 / span 2; }
        .k-metrics { grid-column: 2; grid-row: 1; }
        .r-activity { grid-column: 3; grid-row: 1; }
        .g-chart { grid-column: 2; grid-row: 2; }
        .t-overview { grid-column: 3; grid-row: 2; }

        /* Chart */
        .chart-box {
            position: relative;
            flex: 1;
            margin-top: 20px;
            min-height: 140px;
        }
        .chart-tooltip {
            position: absolute;
            right: 15%;
            top: 25%;
            background-color: #FFFFFF;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            z-index: 10;
        }
    </style>
</head>
<body>

    <div class="window">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-notch"></div>
            
            <div class="logo-box"></div>
            
            <!-- Home -->
            <div class="nav-item active">
                <i data-lucide="layout" style="width:20px;height:20px;stroke-width:2.5;"></i>
            </div>
            <!-- Folder -->
            <div class="nav-item">
                <i data-lucide="folder" style="width:20px;height:20px;stroke-width:2;"></i>
            </div>
            <!-- Users -->
            <div class="nav-item">
                <i data-lucide="users" style="width:20px;height:20px;stroke-width:2;"></i>
            </div>
            <!-- Chart -->
            <div class="nav-item">
                <i data-lucide="bar-chart-2" style="width:20px;height:20px;stroke-width:2;"></i>
            </div>
            <!-- Settings -->
            <div class="nav-item">
                <i data-lucide="settings" style="width:20px;height:20px;stroke-width:2;"></i>
            </div>
        </div>

        <!-- Workspace -->
        <div class="workspace">
            
            <div class="header">
                <h1>Dashboard Overview</h1>
                <div class="header-right">
                    <span class="date">Monday, Oct 23, 10:09 AM</span>
                    <div class="lang-pill">
                        ES 
                        <i data-lucide="chevron-down" style="width:14px;height:14px;stroke-width:2.5;"></i>
                    </div>
                </div>
            </div>

            <div class="grid">
                
                <!-- Performance Summary -->
                <div class="card p-summary">
                    <div class="card-header">
                        <div class="card-title">Performance Summary</div>
                    </div>
                    
                    <div class="metric-group">
                        <div class="label">Total Revenue</div>
                        <div class="metric-value-row">
                            <span class="big-number">$87,450.00</span>
                            <span class="indicator green"><i data-lucide="arrow-up-right"></i> +12.4%</span>
                        </div>
                    </div>

                    <div class="metric-group">
                        <div class="label">New MRR</div>
                        <div class="metric-value-row">
                            <span class="big-number">$14,210.00</span>
                            <span class="indicator green"><i data-lucide="arrow-up-right"></i> +8.2%</span>
                        </div>
                    </div>

                    <div class="metric-group" style="margin-bottom:0;">
                        <div class="label">Active Users</div>
                        <div class="metric-value-row">
                            <span class="big-number">1,894</span>
                            <span class="indicator red"><i data-lucide="arrow-down-right"></i> -1.1%</span>
                        </div>
                    </div>
                </div>

                <!-- Key Metrics -->
                <div class="card k-metrics">
                    <div class="card-header">
                        <div class="card-title">Key Metrics</div>
                        <i data-lucide="more-horizontal" class="more-dots"></i>
                    </div>
                    
                    <div class="progress-bar-container">
                        <div class="label">Project Pulse</div>
                        <div class="pulse-text">84% Complete</div>
                        <div class="segments">
                            <div class="segment"></div>
                            <div class="segment"></div>
                            <div class="segment"></div>
                            <div class="segment half"></div>
                            <div class="segment empty"></div>
                        </div>
                        <div class="segment-labels">
                            <span>|</span>
                            <span>|</span>
                            <span>80%</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 32px;">
                        <div class="label">Client Health</div>
                        <div style="font-size:26px; font-weight:800; color:var(--text-main);">Healthy</div>
                    </div>
                </div>

                <!-- Recent Activity -->
                <div class="card r-activity">
                    <div class="card-header">
                        <div class="card-title">Recent Activity</div>
                        <i data-lucide="more-horizontal" class="more-dots"></i>
                    </div>
                    
                    <div class="activity-row">
                        <div>
                            <div class="act-title">Onboarded:</div>
                            <div class="act-name">Alice Chen</div>
                        </div>
                        <div class="act-time">4h ago</div>
                    </div>
                    
                    <div class="activity-row">
                        <div>
                            <div class="act-title">Milestone:</div>
                            <div class="act-name">Gamma launched</div>
                        </div>
                        <div class="act-time">6h ago</div>
                    </div>
                    
                    <div class="activity-row">
                        <div>
                            <div class="act-title">Task:</div>
                            <div class="act-name">Project Review</div>
                        </div>
                        <div class="act-time">8h ago</div>
                    </div>
                </div>

                <!-- Growth Chart -->
                <div class="card g-chart">
                    <div class="card-header" style="margin-bottom:8px;">
                        <div class="card-title">Growth Chart</div>
                        <i data-lucide="more-horizontal" class="more-dots"></i>
                    </div>
                    <div class="label">Monthly Growth</div>
                    
                    <div class="chart-box">
                        <div class="chart-tooltip">$16.8k</div>
                        <svg width="100%" height="100%" viewBox="0 0 400 120" preserveAspectRatio="none">
                            <defs>
                                <linearGradient id="fillGrad" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="#6C737E" stop-opacity="0.2" />
                                    <stop offset="100%" stop-color="#6C737E" stop-opacity="0" />
                                </linearGradient>
                            </defs>
                            
                            <!-- Grid Lines -->
                            <line x1="40" y1="20" x2="400" y2="20" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            <line x1="40" y1="50" x2="400" y2="50" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            <line x1="40" y1="80" x2="400" y2="80" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            
                            <!-- Y Axis Text -->
                            <text x="10" y="24" fill="#A0A5AE" font-size="11" font-weight="600">18k</text>
                            <text x="10" y="54" fill="#A0A5AE" font-size="11" font-weight="600">16k</text>
                            <text x="10" y="84" fill="#A0A5AE" font-size="11" font-weight="600">14k</text>
                            <text x="10" y="114" fill="#A0A5AE" font-size="11" font-weight="600">12k</text>
                            
                            <!-- Chart Area -->
                            <path d="M 40,80 C 100,20 150,50 200,40 C 250,30 300,10 350,20 L 350,110 L 40,110 Z" fill="url(#fillGrad)"/>
                            <path d="M 40,80 C 100,20 150,50 200,40 C 250,30 300,10 350,20" fill="none" stroke="#2B2F33" stroke-width="2.5" stroke-linecap="round"/>
                            
                            <!-- Data Dots -->
                            <circle cx="125" cy="44" r="4.5" fill="#F3EFE6" stroke="#2B2F33" stroke-width="2.5"/>
                            <circle cx="205" cy="38" r="4.5" fill="#F3EFE6" stroke="#2B2F33" stroke-width="2.5"/>
                            <circle cx="330" cy="18" r="4.5" fill="#F3EFE6" stroke="#2B2F33" stroke-width="2.5"/>
                            
                            <!-- X Axis Text -->
                            <text x="40" y="116" fill="#A0A5AE" font-size="11" font-weight="600">Jul</text>
                            <text x="125" y="116" fill="#A0A5AE" font-size="11" font-weight="600">Aug</text>
                            <text x="205" y="116" fill="#A0A5AE" font-size="11" font-weight="600">Sep</text>
                            <text x="330" y="116" fill="#A0A5AE" font-size="11" font-weight="600">Oct</text>
                        </svg>
                    </div>
                </div>

                <!-- Team Overview -->
                <div class="card t-overview">
                    <div class="card-header">
                        <div class="card-title">Team Overview</div>
                        <i data-lucide="more-horizontal" class="more-dots"></i>
                    </div>
                    
                    <div class="team-row">
                        <div class="avatar">ES</div>
                        <div>
                            <div class="act-name">Active</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-row">
                        <div class="avatar">AB</div>
                        <div>
                            <div class="act-name">Active</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-row">
                        <div class="avatar">CJ</div>
                        <div>
                            <div class="act-name">Members</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-row">
                        <div class="avatar">ML</div>
                        <div>
                            <div class="act-name">Roles</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    build_exact_clone_3()

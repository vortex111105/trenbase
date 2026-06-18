def build_exact_clone_2():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        body {
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background-color: #e8e4db;
        }

        /* The overall floating window (Unified Frosted Glass) */
        .window {
            background: rgba(246, 242, 235, 0.75); /* Exact creamy frosted glass */
            backdrop-filter: blur(45px);
            -webkit-backdrop-filter: blur(45px);
            width: 95vw;
            max-width: 1200px;
            height: 85vh;
            max-height: 800px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.4); /* Very subtle outer edge */
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.08),
                inset 0 1px 1px rgba(255, 255, 255, 0.8);
            display: flex;
            position: relative;
            overflow: hidden;
        }

        /* Sidebar - No solid background, it's part of the glass window */
        .sidebar {
            width: 80px;
            border-right: 1px solid rgba(0, 0, 0, 0.03);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 24px 0;
            position: relative;
            z-index: 10;
        }

        /* The little dark edge indicator on the left of the active icon */
        .edge-indicator {
            position: absolute;
            left: 0;
            top: 102px; /* Aligned with the active icon */
            width: 4px;
            height: 32px;
            background: #2D3135;
            border-radius: 0 4px 4px 0;
        }

        .logo {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #4A4E53, #1E2124);
            border-radius: 10px;
            margin-bottom: 40px;
            position: relative;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }
        
        .logo::after {
            content: '';
            position: absolute;
            top: 0; right: 0;
            width: 100%; height: 100%;
            background: rgba(255,255,255,0.2);
            clip-path: polygon(100% 0, 100% 50%, 0 100%, 0 0);
            border-radius: 10px;
        }

        .nav-item {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
            border-radius: 12px;
            cursor: pointer;
            transition: 0.2s;
            color: #8A8F98;
        }

        .nav-item.active {
            background: #2D3135;
            color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        .nav-item svg { width: 20px; height: 20px; stroke-width: 2; }

        /* Main Content */
        .main-content {
            flex: 1;
            padding: 24px 40px;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        /* Header - Part of the glass window, NO solid background */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            position: relative;
            z-index: 10;
            padding-top: 8px;
        }

        .header h1 {
            font-size: 22px;
            font-weight: 700;
            color: #1A1D21;
            letter-spacing: -0.5px;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .date-text {
            font-size: 13px;
            color: #6B7280;
            font-weight: 500;
        }

        .lang-selector {
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(228, 223, 211, 0.6); /* Translucent pill */
            padding: 6px 12px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: 700;
            color: #1A1D21;
            cursor: pointer;
            box-shadow: inset 0 1px 2px rgba(255,255,255,0.8);
        }

        /* Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1.1fr 1fr 1fr;
            grid-template-rows: auto auto;
            gap: 20px;
            flex: 1;
            padding-bottom: 24px;
        }

        /* Neumorphic Cards - Soft Extrusion */
        .card {
            background: #EBE6DA; /* Matches the window closely but solid enough to pop */
            border-radius: 20px;
            padding: 24px;
            border: none;
            /* The perfect neumorphic puff: sharp bright top-left, soft dark bottom-right */
            box-shadow: 
                -6px -6px 16px rgba(255, 255, 255, 0.8),
                6px 6px 16px rgba(0, 0, 0, 0.04);
            position: relative;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-1px);
            box-shadow: 
                -8px -8px 20px rgba(255, 255, 255, 0.9),
                8px 8px 20px rgba(0, 0, 0, 0.05);
        }

        .card-title {
            font-size: 15px;
            font-weight: 600;
            color: #1A1D21;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .more-icon {
            color: #9CA3AF;
            cursor: pointer;
        }

        /* Typography */
        .label {
            font-size: 12px;
            color: #6B7280;
            font-weight: 500;
            margin-bottom: 2px;
        }
        
        .big-value {
            font-size: 26px;
            font-weight: 700;
            color: #1A1D21;
            letter-spacing: -0.5px;
            margin-right: 8px;
        }
        
        .indicator {
            font-size: 11px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 2px;
        }
        .text-green { color: #2E9E44; }
        .text-red { color: #D92D20; }
        
        .metric-row {
            margin-bottom: 24px;
            display: flex;
            align-items: baseline;
        }

        /* Progress Bar */
        .pulse-track {
            display: flex;
            gap: 4px;
            margin-top: 8px;
            margin-bottom: 6px;
        }
        .pulse-seg {
            height: 6px;
            border-radius: 3px;
            background: #6B7280;
            flex: 1;
        }
        .pulse-seg.half {
            background: linear-gradient(90deg, #6B7280 50%, #D4D0C5 50%);
        }
        .pulse-seg.empty {
            background: #D4D0C5;
        }
        .pulse-labels {
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #9CA3AF;
            font-weight: 600;
        }

        /* Activity List */
        .activity-item {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 18px;
        }
        .activity-item:last-child { margin-bottom: 0; }
        .act-title { font-size: 12px; color: #6B7280; margin-bottom: 2px; }
        .act-desc { font-size: 13px; font-weight: 600; color: #1A1D21; }
        .act-time { font-size: 11px; color: #9CA3AF; }

        /* Avatars */
        .team-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }
        .team-item:last-child { margin-bottom: 0; }
        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #E4DFD3;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            color: #1A1D21;
            /* Inner shadow for neumorphic indent */
            box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.05), inset -2px -2px 4px rgba(255, 255, 255, 0.8);
        }

        /* Specific Card Placements */
        .card-perf { grid-column: 1; grid-row: 1 / span 2; }
        .card-metrics { grid-column: 2; grid-row: 1; }
        .card-activity { grid-column: 3; grid-row: 1; }
        .card-growth { grid-column: 2; grid-row: 2; }
        .card-team { grid-column: 3; grid-row: 2; }
        
        /* The chart */
        .chart-container {
            position: relative;
            flex: 1;
            margin-top: 10px;
            margin-left: -10px; /* Shift left to align with labels */
        }
        
        /* Tooltip */
        .tooltip {
            position: absolute;
            right: 10%;
            top: 25%;
            background: #FFFFFF;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            z-index: 10;
        }
    </style>
</head>
<body>

    <div class="window">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="edge-indicator"></div>
            
            <div class="logo"></div>
            
            <!-- Home -->
            <div class="nav-item active">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
            </div>
            <!-- Folder -->
            <div class="nav-item">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
            </div>
            <!-- Users -->
            <div class="nav-item">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            </div>
            <!-- Chart -->
            <div class="nav-item">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
            </div>
            <!-- Settings -->
            <div class="nav-item">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            
            <div class="header">
                <h1>Dashboard Overview</h1>
                <div class="header-right">
                    <span class="date-text">Monday, Oct 23, 10:09 AM</span>
                    <div class="lang-selector">
                        ES 
                        <svg width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid">
                
                <!-- Performance Summary -->
                <div class="card card-perf">
                    <div class="card-title">Performance Summary</div>
                    
                    <div class="label mt-2">Total Revenue</div>
                    <div class="metric-row">
                        <span class="big-value">$87,450.00</span>
                        <span class="indicator text-green">
                            <svg width="10" height="10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 15l7-7 7 7"></path></svg> 
                            +12.4%
                        </span>
                    </div>

                    <div class="label">New MRR</div>
                    <div class="metric-row">
                        <span class="big-value">$14,210.00</span>
                        <span class="indicator text-green">
                            <svg width="10" height="10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 15l7-7 7 7"></path></svg> 
                            +8.2%
                        </span>
                    </div>

                    <div class="label">Active Users</div>
                    <div class="metric-row" style="margin-bottom:0;">
                        <span class="big-value">1,894</span>
                        <span class="indicator text-red">
                            <svg width="10" height="10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"></path></svg> 
                            -1.1%
                        </span>
                    </div>
                </div>

                <!-- Key Metrics -->
                <div class="card card-metrics">
                    <div class="card-title">
                        Key Metrics
                        <svg class="more-icon" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
                    </div>
                    
                    <div class="label">Project Pulse</div>
                    <div style="font-size:13px; font-weight:600; color:#1A1D21; margin-bottom: 2px;">84% Complete</div>
                    <div class="pulse-track">
                        <div class="pulse-seg"></div>
                        <div class="pulse-seg"></div>
                        <div class="pulse-seg"></div>
                        <div class="pulse-seg half"></div>
                        <div class="pulse-seg empty"></div>
                    </div>
                    <div class="pulse-labels">
                        <span>I</span>
                        <span>I</span>
                        <span>80%</span>
                    </div>
                    
                    <div class="label" style="margin-top: 20px;">Client Health</div>
                    <div style="font-size:22px; font-weight:700; color:#1A1D21;">Healthy</div>
                </div>

                <!-- Recent Activity -->
                <div class="card card-activity">
                    <div class="card-title">
                        Recent Activity
                        <svg class="more-icon" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
                    </div>
                    
                    <div class="activity-item">
                        <div>
                            <div class="act-title">Onboarded:</div>
                            <div class="act-desc">Alice Chen</div>
                        </div>
                        <div class="act-time">4h ago</div>
                    </div>
                    
                    <div class="activity-item">
                        <div>
                            <div class="act-title">Milestone:</div>
                            <div class="act-desc">Gamma launched</div>
                        </div>
                        <div class="act-time">6h ago</div>
                    </div>
                    
                    <div class="activity-item">
                        <div>
                            <div class="act-title">Task:</div>
                            <div class="act-desc">Project Review</div>
                        </div>
                        <div class="act-time">8h ago</div>
                    </div>
                </div>

                <!-- Growth Chart -->
                <div class="card card-growth">
                    <div class="card-title" style="margin-bottom:8px;">
                        Growth Chart
                        <svg class="more-icon" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
                    </div>
                    <div class="label">Monthly Growth</div>
                    
                    <div class="chart-container">
                        <div class="tooltip">$16.8k</div>
                        
                        <!-- Clean Real SVG -->
                        <svg width="100%" height="100%" viewBox="0 0 400 120" preserveAspectRatio="none" style="position:relative; z-index:2;">
                            <defs>
                                <linearGradient id="fillGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="#2D3135" stop-opacity="0.10" />
                                    <stop offset="100%" stop-color="#2D3135" stop-opacity="0" />
                                </linearGradient>
                            </defs>
                            <!-- Horizontal lines -->
                            <line x1="40" y1="20" x2="380" y2="20" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            <line x1="40" y1="50" x2="380" y2="50" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            <line x1="40" y1="80" x2="380" y2="80" stroke="#000" stroke-opacity="0.05" stroke-width="1"/>
                            
                            <!-- Y Labels -->
                            <text x="15" y="23" fill="#9CA3AF" font-size="10" font-weight="600">18k</text>
                            <text x="15" y="53" fill="#9CA3AF" font-size="10" font-weight="600">16k</text>
                            <text x="15" y="83" fill="#9CA3AF" font-size="10" font-weight="600">14k</text>
                            <text x="15" y="113" fill="#9CA3AF" font-size="10" font-weight="600">12k</text>
                            
                            <!-- Area fill -->
                            <path d="M 40,80 C 100,20 150,50 200,40 C 250,30 300,10 350,20 L 350,110 L 40,110 Z" fill="url(#fillGradient)"/>
                            <!-- Line stroke -->
                            <path d="M 40,80 C 100,20 150,50 200,40 C 250,30 300,10 350,20" fill="none" stroke="#2D3135" stroke-width="2" stroke-linecap="round"/>
                            
                            <!-- Dots -->
                            <circle cx="130" cy="45" r="4" fill="#EFEBE1" stroke="#2D3135" stroke-width="2"/>
                            <circle cx="210" cy="38" r="4" fill="#EFEBE1" stroke="#2D3135" stroke-width="2"/>
                            <circle cx="330" cy="18" r="4" fill="#EFEBE1" stroke="#2D3135" stroke-width="2"/>
                            
                            <!-- X Labels -->
                            <text x="40" y="115" fill="#9CA3AF" font-size="10" font-weight="600">Jul</text>
                            <text x="130" y="115" fill="#9CA3AF" font-size="10" font-weight="600">Aug</text>
                            <text x="210" y="115" fill="#9CA3AF" font-size="10" font-weight="600">Sep</text>
                            <text x="330" y="115" fill="#9CA3AF" font-size="10" font-weight="600">Oct</text>
                        </svg>
                    </div>
                </div>

                <!-- Team Overview -->
                <div class="card card-team">
                    <div class="card-title">
                        Team Overview
                        <svg class="more-icon" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
                    </div>
                    
                    <div class="team-item">
                        <div class="avatar">ES</div>
                        <div>
                            <div class="act-desc">Active</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-item">
                        <div class="avatar">AB</div>
                        <div>
                            <div class="act-desc">Active</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-item">
                        <div class="avatar">CJ</div>
                        <div>
                            <div class="act-desc">Members</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                    
                    <div class="team-item">
                        <div class="avatar">ML</div>
                        <div>
                            <div class="act-desc">Roles</div>
                            <div class="act-title" style="margin:0;">Online</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    build_exact_clone_2()

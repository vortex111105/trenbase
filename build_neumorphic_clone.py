def build_clone():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neumorphic Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Inter', sans-serif;
            color: #2D3135;
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100vh; 
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Subtle warm dimming overlay */
        body::after {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(240, 235, 225, 0.4); 
            z-index: -1;
        }

        /* The Main Window */
        .glass-window {
            background: rgba(246, 243, 237, 0.95); /* Creamy off-white */
            backdrop-filter: blur(40px);
            -webkit-backdrop-filter: blur(40px);
            border-radius: 40px;
            box-shadow: 
                0 40px 80px rgba(0, 0, 0, 0.08),
                0 15px 35px rgba(0, 0, 0, 0.04),
                inset 0 2px 4px rgba(255, 255, 255, 1),
                inset 2px 0 4px rgba(255, 255, 255, 0.5);
            width: 90vw;
            max-width: 1400px;
            height: 85vh;
            display: flex;
            overflow: hidden;
        }

        /* Neumorphic Cards */
        .neo-card {
            background: #F6F3ED; /* Match the window background */
            border-radius: 32px;
            /* Neumorphism: bright top-left, dark bottom-right */
            box-shadow: 
                -8px -8px 20px rgba(255, 255, 255, 1),
                8px 8px 20px rgba(0, 0, 0, 0.05);
            padding: 28px;
            display: flex;
            flex-direction: column;
        }

        /* For inner shadows (pressed state, or chart areas) */
        .neo-inner {
            background: #F6F3ED;
            border-radius: 12px;
            box-shadow: 
                inset 4px 4px 8px rgba(0, 0, 0, 0.05),
                inset -4px -4px 8px rgba(255, 255, 255, 1);
        }

        /* Text Styles */
        .title-main { font-weight: 700; font-size: 1.5rem; letter-spacing: -0.03em; color: #1E2124; }
        .card-title { font-weight: 600; font-size: 1.05rem; color: #2D3135; margin-bottom: 20px; }
        .sub-text { font-size: 0.8rem; color: #6F767E; font-weight: 500; }
        .big-money { font-size: 2.5rem; font-weight: 700; color: #1E2124; letter-spacing: -0.05em; line-height: 1.1; }
        
        .indicator-green { color: #2EA043; font-weight: 600; font-size: 0.85rem; }
        .indicator-red { color: #E03131; font-weight: 600; font-size: 0.85rem; }

        /* Sidebar active item */
        .sidebar-item { color: #6F767E; padding: 12px; border-radius: 16px; transition: all 0.2s; cursor: pointer; }
        .sidebar-item:hover { color: #1E2124; background: rgba(0,0,0,0.03); }
        .sidebar-active { background: #2D3135 !important; color: white !important; box-shadow: 0 8px 16px rgba(0,0,0,0.1); }

        .divider { height: 1px; background: rgba(0,0,0,0.04); margin: 16px 0; }
        
        /* The chart curve */
        .chart-svg {
            width: 100%;
            height: 100px;
            margin-top: 20px;
        }
        
        /* Progress segments */
        .pulse-seg {
            height: 8px;
            background: #6F767E;
            border-radius: 4px;
            flex: 1;
        }
        .pulse-seg.empty { background: rgba(0,0,0,0.06); }
        .pulse-seg.half { background: linear-gradient(to right, #6F767E 50%, rgba(0,0,0,0.06) 50%); }

        /* Avatars */
        .avatar {
            width: 36px; height: 36px;
            border-radius: 50%;
            background: #E8E4DB;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.8rem; color: #2D3135;
            box-shadow: inset 1px 1px 3px rgba(0,0,0,0.05), -2px -2px 5px rgba(255,255,255,0.8);
        }
    </style>
</head>
<body>

    <div class="glass-window">
        <!-- Sidebar -->
        <div class="w-[100px] border-r border-[rgba(0,0,0,0.04)] flex flex-col items-center py-10 gap-8 relative">
            <!-- Brand Logo Mark -->
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-gray-700 to-black shadow-lg mb-4 flex-shrink-0">
                <div class="w-full h-full rounded-xl bg-white/20" style="clip-path: polygon(0 0, 100% 0, 100% 50%, 0 100%);"></div>
            </div>
            
            <div class="flex flex-col gap-4 w-full px-6">
                <div class="sidebar-item sidebar-active flex justify-center"><i data-lucide="layout-grid" class="w-6 h-6"></i></div>
                <div class="sidebar-item flex justify-center"><i data-lucide="folder" class="w-6 h-6"></i></div>
                <div class="sidebar-item flex justify-center"><i data-lucide="users" class="w-6 h-6"></i></div>
                <div class="sidebar-item flex justify-center"><i data-lucide="bar-chart-2" class="w-6 h-6"></i></div>
                <div class="sidebar-item flex justify-center"><i data-lucide="settings" class="w-6 h-6"></i></div>
            </div>
            
            <!-- A subtle notch/handle on the far left edge like the image -->
            <div class="absolute left-0 top-32 w-1.5 h-16 bg-[#2D3135] rounded-r-lg opacity-80"></div>
        </div>

        <!-- Main Content Area -->
        <div class="flex-1 flex flex-col p-10 overflow-hidden">
            
            <!-- Header -->
            <div class="flex justify-between items-end mb-10">
                <h1 class="title-main text-[1.8rem]">Dashboard Overview</h1>
                <div class="flex items-center gap-4">
                    <span class="sub-text">Monday, Oct 23, 10:09 AM</span>
                    <div class="neo-inner px-4 py-2 flex items-center gap-2 cursor-pointer">
                        <span class="font-bold text-sm">ES</span>
                        <i data-lucide="chevron-down" class="w-4 h-4 text-gray-400"></i>
                    </div>
                </div>
            </div>

            <!-- Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-[1.2fr_1fr_1fr] gap-8 h-full overflow-y-auto pr-4 pb-4">
                
                <!-- Performance Summary (Col 1, spans 2 rows visually, we'll use flex/grid to match) -->
                <div class="neo-card flex flex-col gap-6 row-span-2">
                    <h2 class="card-title mb-0">Performance Summary</h2>
                    
                    <div>
                        <div class="sub-text mb-1">Total Revenue</div>
                        <div class="flex items-baseline gap-3">
                            <span class="big-money">$87,450.00</span>
                            <span class="indicator-green flex items-center gap-1"><i data-lucide="arrow-up-right" class="w-3 h-3"></i> +12.4%</span>
                        </div>
                    </div>
                    
                    <div>
                        <div class="sub-text mb-1">New MRR</div>
                        <div class="flex items-baseline gap-3">
                            <span class="big-money">$14,210.00</span>
                            <span class="indicator-green flex items-center gap-1"><i data-lucide="arrow-up-right" class="w-3 h-3"></i> +8.2%</span>
                        </div>
                    </div>
                    
                    <div>
                        <div class="sub-text mb-1">Active Users</div>
                        <div class="flex items-baseline gap-3">
                            <span class="big-money">1,894</span>
                            <span class="indicator-red flex items-center gap-1"><i data-lucide="arrow-down-right" class="w-3 h-3"></i> -1.1%</span>
                        </div>
                    </div>
                </div>

                <!-- Key Metrics (Col 2, Row 1) -->
                <div class="neo-card justify-between relative">
                    <button class="absolute top-6 right-6 text-gray-400 hover:text-gray-600"><i data-lucide="more-horizontal" class="w-5 h-5"></i></button>
                    
                    <div>
                        <h2 class="card-title">Key Metrics</h2>
                        
                        <div class="sub-text mb-1">Project Pulse</div>
                        <div class="font-bold text-gray-800 mb-3">84% Complete</div>
                        <div class="flex gap-1.5 mb-2">
                            <div class="pulse-seg"></div>
                            <div class="pulse-seg"></div>
                            <div class="pulse-seg"></div>
                            <div class="pulse-seg half"></div>
                            <div class="pulse-seg empty"></div>
                        </div>
                        <div class="flex justify-between text-[10px] text-gray-400 font-bold mb-6">
                            <span>|</span><span>|</span><span>80%</span>
                        </div>
                        
                        <div class="sub-text mb-1">Client Health</div>
                        <div class="text-3xl font-extrabold text-[#1E2124] tracking-tight">Healthy</div>
                    </div>
                </div>

                <!-- Recent Activity (Col 3, Row 1) -->
                <div class="neo-card relative">
                    <button class="absolute top-6 right-6 text-gray-400 hover:text-gray-600"><i data-lucide="more-horizontal" class="w-5 h-5"></i></button>
                    <h2 class="card-title">Recent Activity</h2>
                    
                    <div class="flex flex-col gap-5">
                        <div class="flex justify-between items-start">
                            <div>
                                <div class="sub-text">Onboarded:</div>
                                <div class="font-semibold text-gray-800">Alice Chen</div>
                            </div>
                            <span class="sub-text text-xs mt-1">4h ago</span>
                        </div>
                        <div class="divider my-0"></div>
                        <div class="flex justify-between items-start">
                            <div>
                                <div class="sub-text">Milestone:</div>
                                <div class="font-semibold text-gray-800">Gamma launched</div>
                            </div>
                            <span class="sub-text text-xs mt-1">6h ago</span>
                        </div>
                        <div class="divider my-0"></div>
                        <div class="flex justify-between items-start">
                            <div>
                                <div class="sub-text">Task:</div>
                                <div class="font-semibold text-gray-800">Project Review</div>
                            </div>
                            <span class="sub-text text-xs mt-1">8h ago</span>
                        </div>
                    </div>
                </div>

                <!-- Growth Chart (Col 2 & 3, Row 2) -->
                <div class="neo-card col-span-1 md:col-span-2 relative">
                    <button class="absolute top-6 right-6 text-gray-400 hover:text-gray-600"><i data-lucide="more-horizontal" class="w-5 h-5"></i></button>
                    <h2 class="card-title mb-1">Growth Chart</h2>
                    <div class="sub-text mb-6">Monthly Growth</div>
                    
                    <div class="relative flex-1 mt-auto">
                        <!-- Y Axis Labels -->
                        <div class="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-400 font-semibold pb-6 z-10">
                            <span>18k</span>
                            <span>16k</span>
                            <span>14k</span>
                            <span>12k</span>
                        </div>
                        
                        <!-- Chart Lines (horizontal) -->
                        <div class="absolute left-8 right-0 top-0 h-full flex flex-col justify-between pb-6">
                            <div class="w-full h-[1px] bg-black/5"></div>
                            <div class="w-full h-[1px] bg-black/5"></div>
                            <div class="w-full h-[1px] bg-black/5"></div>
                            <div class="w-full h-[1px] bg-black/5"></div>
                        </div>

                        <!-- SVG Curve -->
                        <div class="absolute left-8 right-0 top-0 bottom-6">
                            <svg class="w-full h-full" preserveAspectRatio="none" viewBox="0 0 400 100">
                                <!-- Gradient fill -->
                                <defs>
                                    <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stop-color="#2D3135" stop-opacity="0.15" />
                                        <stop offset="100%" stop-color="#2D3135" stop-opacity="0" />
                                    </linearGradient>
                                </defs>
                                <path d="M 0,80 C 40,30 80,40 120,40 C 160,40 180,20 220,30 C 260,40 300,-10 350,10 L 350,100 L 0,100 Z" fill="url(#chartGradient)"/>
                                <!-- The thick line -->
                                <path d="M 0,80 C 40,30 80,40 120,40 C 160,40 180,20 220,30 C 260,40 300,-10 350,10" fill="none" stroke="#2D3135" stroke-width="3" stroke-linecap="round"/>
                                
                                <!-- Data points -->
                                <circle cx="120" cy="40" r="4" fill="#F6F3ED" stroke="#2D3135" stroke-width="2"/>
                                <circle cx="220" cy="30" r="4" fill="#F6F3ED" stroke="#2D3135" stroke-width="2"/>
                                <circle cx="300" cy="-2" r="4" fill="#F6F3ED" stroke="#2D3135" stroke-width="2"/>
                            </svg>
                        </div>
                        
                        <!-- Tooltip on the chart -->
                        <div class="absolute right-[10%] top-[5%] neo-inner px-3 py-1.5 shadow-md border border-white/50 text-sm font-bold text-gray-800 z-20">
                            $16.8k
                        </div>

                        <!-- X Axis Labels -->
                        <div class="absolute left-8 right-0 bottom-0 flex justify-between text-xs text-gray-400 font-semibold px-4">
                            <span>Jul</span>
                            <span>Aug</span>
                            <span>Sep</span>
                            <span>Oct</span>
                        </div>
                    </div>
                </div>

                <!-- Team Overview (Col 4, Row 2 / Wait, the image has Col 3 split into two vertically? No, Team Overview is below Recent Activity. 
                     The grid is Col 1 (Performance), Col 2 (Key Metrics over Growth Chart), Col 3 (Recent Activity over Team Overview).
                     Let's adjust grid flow to match the image: Performance is tall on the left.
                     Middle is Key Metrics (top) and Growth Chart (bottom, but Growth Chart is WIDE).
                     Actually, Growth Chart spans the middle and right columns!
                     Image Layout:
                     Row 1: [Performance] [Key Metrics] [Recent Activity]
                     Row 2: [Performance] [       Growth Chart      ] [Team Overview]
                     Wait, looking at the image:
                     Left: Performance Summary (Tall)
                     Middle Top: Key Metrics
                     Right Top: Recent Activity
                     Bottom Left(ish): Growth Chart (Wide)
                     Bottom Right: Team Overview
                     Yes! Growth chart is below Performance? No, Performance spans both rows!
                     So Growth Chart spans Middle and Right?
                     Let's look at the image again:
                     Growth chart is below Performance and Key Metrics? No, Performance is on the left.
                     Wait, the image grid is:
                     Row 1: Performance Summary (Left), Key Metrics (Middle), Recent Activity (Right)
                     Row 2: Growth Chart (Left & Middle??), Team Overview (Right)
                     Ah! Performance Summary is NOT tall enough to span two rows. It's just Row 1 Left.
                     But Growth Chart is UNDER Performance Summary?
                     Let's look at the edges.
                     Growth Chart is under Performance Summary AND Key Metrics. It spans 2 columns.
                     Team Overview is under Recent Activity. It spans 1 column.
                     Yes! Grid:
                     Col 1 & 2: Growth chart
                     Col 3: Team Overview
                -->
            </div>
            
            <!-- Fixing the grid explicitly to match the image -->
            <style>
                .custom-grid {
                    display: grid;
                    grid-template-columns: 1.2fr 1fr 1fr;
                    grid-template-rows: auto auto;
                    gap: 32px;
                    height: 100%;
                }
                .perf-card { grid-column: 1; grid-row: 1; }
                .metrics-card { grid-column: 2; grid-row: 1; }
                .activity-card { grid-column: 3; grid-row: 1; }
                .growth-card { grid-column: 1 / span 2; grid-row: 2; }
                .team-card { grid-column: 3; grid-row: 2; }
            </style>
            
        </div>
    </div>
    
    <script>
        // Apply custom grid fix
        document.querySelector('.grid').classList.remove('grid', 'grid-cols-1', 'md:grid-cols-3', 'lg:grid-cols-[1.2fr_1fr_1fr]', 'gap-8');
        document.querySelector('.grid').classList.add('custom-grid');
        
        const cards = document.querySelectorAll('.neo-card');
        cards[0].classList.add('perf-card');
        cards[0].classList.remove('row-span-2');
        cards[1].classList.add('metrics-card');
        cards[2].classList.add('activity-card');
        cards[3].classList.add('growth-card');
        cards[3].classList.remove('col-span-1', 'md:col-span-2');
        
        // Let's add the Team Overview card dynamically since we didn't finish it in the layout above
        const teamCardHTML = `
        <div class="neo-card team-card relative">
            <button class="absolute top-6 right-6 text-gray-400 hover:text-gray-600"><i data-lucide="more-horizontal" class="w-5 h-5"></i></button>
            <h2 class="card-title">Team Overview</h2>
            
            <div class="flex flex-col gap-5 mt-2">
                <div class="flex items-center gap-4">
                    <div class="avatar">ES</div>
                    <div>
                        <div class="font-bold text-gray-800 text-sm">Active</div>
                        <div class="sub-text">Online</div>
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <div class="avatar">AB</div>
                    <div>
                        <div class="font-bold text-gray-800 text-sm">Active</div>
                        <div class="sub-text">Online</div>
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <div class="avatar">CJ</div>
                    <div>
                        <div class="font-bold text-gray-800 text-sm">Members</div>
                        <div class="sub-text">Online</div>
                    </div>
                </div>
                <div class="flex items-center gap-4">
                    <div class="avatar">ML</div>
                    <div>
                        <div class="font-bold text-gray-800 text-sm">Roles</div>
                        <div class="sub-text">Online</div>
                    </div>
                </div>
            </div>
        </div>`;
        
        document.querySelector('.custom-grid').insertAdjacentHTML('beforeend', teamCardHTML);
        
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    build_clone()

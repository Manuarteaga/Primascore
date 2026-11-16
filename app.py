import streamlit as st

# Configuración de la página en modo ancho (wide)
st.set_page_config(
    page_title="PrimaScore | Evaluador de Opcionabilidad",
    page_icon="📈",
    layout="wide",
)

# Código HTML, CSS y JavaScript completo integrado en Streamlit
html_code = """
<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrimaScore | Evaluador de Opcionabilidad para Venta de Primas</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        slate: {
                            850: '#151e32',
                            900: '#0f172a',
                            950: '#090d16',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #090d16;
            color: #f8fafc;
            background-image: 
                radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 50%);
        }
        .glass-card {
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(51, 65, 85, 0.6);
        }
        .score-ring {
            transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.5s ease;
        }
        .bar-fill {
            transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-emerald-500/30 selection:text-emerald-200 p-2 sm:p-4">

    <!-- Navbar -->
    <header class="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30 rounded-xl mb-6">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                    <svg class="w-5 h-5 text-slate-950" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                </div>
                <div>
                    <span class="font-bold text-lg tracking-tight text-white">Prima<span class="text-emerald-400">Score</span></span>
                    <span class="hidden sm:inline-block ml-2 text-[11px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">Wheel & Covered Calls</span>
                </div>
            </div>
            <div class="flex items-center gap-3 text-xs text-slate-400">
                <span class="hidden md:inline">Enfoque: <strong class="text-slate-200">Venta de Primas (Delta 0.30)</strong></span>
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    Simulador Activo
                </span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 max-w-6xl w-full mx-auto px-2 sm:px-6 py-2 space-y-6">

        <!-- Hero & Search Bar -->
        <section class="glass-card rounded-2xl p-5 sm:p-7 shadow-xl">
            <div class="max-w-3xl mx-auto text-center space-y-2 mb-6">
                <h1 class="text-2xl sm:text-3xl font-bold tracking-tight text-white">
                    ¿Vale la pena vender primas en esta acción?
                </h1>
                <p class="text-sm sm:text-base text-slate-400">
                    Analiza al instante la liquidez de la cadena de opciones, el <span class="text-slate-200 font-medium">Bid-Ask Spread</span>, el rendimiento de la prima y el capital requerido por lote (100 acciones).
                </p>
            </div>

            <!-- Search Input -->
            <form id="search-form" class="max-w-xl mx-auto relative">
                <div class="relative flex items-center">
                    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                    <input 
                        type="text" 
                        id="ticker-input" 
                        placeholder="Introduce un ticker (ej. AAPL, F, KO, NVDA, SOFI...)" 
                        maxlength="8"
                        autocomplete="off"
                        class="block w-full pl-11 pr-28 py-3.5 bg-slate-950/90 border border-slate-700 rounded-xl text-white placeholder-slate-500 font-mono uppercase text-base focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all"
                    >
                    <button 
                        type="submit"
                        class="absolute right-2 top-2 bottom-2 px-4 bg-emerald-500 hover:bg-emerald-400 active:scale-95 text-slate-950 font-semibold text-sm rounded-lg transition-all cursor-pointer shadow-md shadow-emerald-500/20">
                        Evaluar
                    </button>
                </div>
            </form>

            <!-- Preset Chips -->
            <div class="max-w-3xl mx-auto mt-4 flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 justify-start sm:justify-center">
                <span class="text-xs text-slate-500 shrink-0 mr-1">Ejemplos:</span>
                <button type="button" onclick="selectTicker('AAPL')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> AAPL
                </button>
                <button type="button" onclick="selectTicker('F')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> F (Ford)
                </button>
                <button type="button" onclick="selectTicker('NVDA')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span> NVDA
                </button>
                <button type="button" onclick="selectTicker('KO')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-amber-400"></span> KO
                </button>
                <button type="button" onclick="selectTicker('ZIM')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-amber-400"></span> ZIM
                </button>
                <button type="button" onclick="selectTicker('ILLQ')" class="preset-btn shrink-0 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition cursor-pointer flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-rose-500"></span> ILLQ (Ilíquida)
                </button>
            </div>
        </section>

        <!-- Dashboard Grid -->
        <div id="dashboard-content" class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Left Column: Overall Score & Verdict (5 cols) -->
            <div class="lg:col-span-5 flex flex-col gap-6">
                <!-- Score Card -->
                <div class="glass-card rounded-2xl p-6 flex flex-col items-center text-center relative overflow-hidden">
                    <!-- Company Header -->
                    <div class="w-full flex items-start justify-between border-b border-slate-800 pb-4 mb-5">
                        <div class="text-left">
                            <div class="flex items-center gap-2">
                                <h2 id="res-ticker" class="text-2xl font-bold font-mono text-white">AAPL</h2>
                                <span id="res-sector" class="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">Tecnología</span>
                            </div>
                            <p id="res-name" class="text-sm text-slate-400 mt-0.5">Apple Inc.</p>
                        </div>
                        <div class="text-right">
                            <div id="res-price" class="text-xl font-bold font-mono text-white">$228.50</div>
                            <div id="res-lot-cost" class="text-xs font-mono text-slate-400">100 acc: <span class="text-slate-200">$22,850</span></div>
                        </div>
                    </div>

                    <!-- Circular Gauge -->
                    <div class="relative w-48 h-48 flex items-center justify-center my-1">
                        <svg class="w-full h-full -rotate-90" viewBox="0 0 120 120">
                            <circle cx="60" cy="60" r="52" fill="none" stroke="#1e293b" stroke-width="10" />
                            <circle id="score-circle" class="score-ring" cx="60" cy="60" r="52" fill="none" stroke="#10b981" stroke-width="10" stroke-linecap="round" stroke-dasharray="326.72" stroke-dashoffset="326.72" />
                        </svg>
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <span class="text-xs uppercase tracking-widest text-slate-400 font-medium">Score</span>
                            <span id="res-score" class="text-5xl font-bold font-mono text-white tracking-tighter my-0.5">92</span>
                            <span class="text-xs font-mono text-slate-500">/ 100 pts</span>
                        </div>
                    </div>

                    <!-- Verdict Badge -->
                    <div id="verdict-badge" class="mt-4 px-4 py-2 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 font-semibold text-sm flex items-center gap-2">
                        <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                        <span id="verdict-text">Altamente Opcionable (Ideal para Primas)</span>
                    </div>

                    <!-- Earnings / Event Warning -->
                    <div id="earnings-banner" class="w-full mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs">
                        <span class="text-slate-400 flex items-center gap-1.5">
                            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                            Próximos Resultados:
                        </span>
                        <span id="res-earnings" class="font-mono font-medium text-slate-200">En 42 días (Seguro)</span>
                    </div>
                </div>

                <!-- Algorithm Diagnosis -->
                <div class="glass-card rounded-2xl p-5 flex-1">
                    <div class="flex items-center gap-2 mb-3">
                        <div class="p-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                        </div>
                        <h3 class="font-semibold text-sm text-white">Diagnóstico para Vendedores de Primas</h3>
                    </div>
                    <ul id="diagnosis-list" class="space-y-2.5 text-xs sm:text-sm text-slate-300 leading-relaxed">
                        <!-- Dynamic items -->
                    </ul>
                </div>
            </div>

            <!-- Right Column: 4 Pillars Breakdown & Simulator (7 cols) -->
            <div class="lg:col-span-7 flex flex-col gap-6">
                
                <!-- 4 Pillars Card -->
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center justify-between mb-5">
                        <h3 class="font-semibold text-base text-white">Desglose de los 4 Pilares de Opcionabilidad</h3>
                        <span class="text-xs font-mono text-slate-400">Ponderación por perfil</span>
                    </div>

                    <div class="space-y-5">
                        <!-- Pillar 1: Liquidity & Spread -->
                        <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="text-sm font-semibold text-white">1. Liquidez y Horquilla (Bid-Ask)</span>
                                    <span class="text-[11px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Peso 35%</span>
                                </div>
                                <span id="p1-score-text" class="font-mono text-sm font-bold text-emerald-400">34 / 35 pts</span>
                            </div>
                            <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden mb-3">
                                <div id="p1-bar" class="bar-fill h-full bg-emerald-400 rounded-full" style="width: 97%"></div>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-xs">
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">Spread ATM</span>
                                    <span id="m-spread" class="font-mono font-semibold text-slate-200">$0.02 (0.6%)</span>
                                </div>
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">Open Interest</span>
                                    <span id="m-oi" class="font-mono font-semibold text-slate-200">48,200</span>
                                </div>
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">Volumen Diario</span>
                                    <span id="m-vol" class="font-mono font-semibold text-slate-200">19,450</span>
                                </div>
                            </div>
                        </div>

                        <!-- Pillar 2: Premium Yield & IV -->
                        <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                            <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="text-sm font-semibold text-white">2. Rentabilidad de la Prima (Yield / IV)</span>
                                    <span class="text-[11px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Peso 30%</span>
                                </div>
                                <span id="p2-score-text" class="font-mono text-sm font-bold text-emerald-400">26 / 30 pts</span>
                            </div>
                            <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden mb-3">
                                <div id="p2-bar" class="bar-fill h-full bg-emerald-400 rounded-full" style="width: 86%"></div>
                            </div>
                            <div class="grid grid-cols-3 gap-2 text-xs">
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">Yield Mensual</span>
                                    <span id="m-yield" class="font-mono font-semibold text-emerald-400">1.65% (~19.8% anual)</span>
                                </div>
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">Volatilidad (IV)</span>
                                    <span id="m-iv" class="font-mono font-semibold text-slate-200">26.4%</span>
                                </div>
                                <div class="bg-slate-900/90 p-2 rounded-lg border border-slate-800/60">
                                    <span class="text-slate-500 block text-[11px]">IV Rank</span>
                                    <span id="m-ivr" class="font-mono font-semibold text-slate-200">38%</span>
                                </div>
                            </div>
                        </div>

                        <!-- Pillar 3 & 4 Grid -->
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <!-- Pillar 3: Capital & Strikes -->
                            <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
                                <div class="flex items-center justify-between gap-1 mb-2">
                                    <span class="text-sm font-semibold text-white">3. Capital y Strikes</span>
                                    <span id="p3-score-text" class="font-mono text-xs font-bold text-emerald-400">17 / 20 pts</span>
                                </div>
             

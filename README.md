# DB_9134_5950

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedStaff Pro | Management System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --med-blue: #2563eb;
            --med-light: #f0f7ff;
        }

        .sidebar-item.active {
            background: var(--med-light);
            color: var(--med-blue);
            border-right: 4px solid var(--med-blue);
        }

        .status-on-call {
            background: #fef3c7;
            color: #92400e;
        }

        .status-active {
            background: #dcfce7;
            color: #166534;
        }

        .shift-card {
            border-left: 4px solid var(--med-blue);
        }
    </style>
</head>

<body class="bg-gray-50 font-sans text-gray-800">

    <div class="flex min-h-screen">
        <!-- Sidebar -->
        <aside class="w-64 bg-white border-r border-gray-200 flex-shrink-0">
            <div class="p-6">
                <h1 class="text-2xl font-bold text-blue-600 flex items-center">
                    <i class="fa-solid fa-house-medical mr-2"></i>MedStaff
                </h1>
            </div>
            <nav class="mt-4">
                <a href="#" onclick="showScreen('dashboard')" id="nav-dashboard"
                    class="sidebar-item active flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 transition">
                    <i class="fa-solid fa-users-gear w-6"></i> Staff Dashboard
                </a>
                <a href="#" onclick="showScreen('scheduling')" id="nav-scheduling"
                    class="sidebar-item flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 transition">
                    <i class="fa-solid fa-calendar-check w-6"></i> Shift Scheduling
                </a>
                <a href="#" onclick="showScreen('departments')" id="nav-departments"
                    class="sidebar-item flex items-center px-6 py-3 text-gray-600 hover:bg-gray-50 transition">
                    <i class="fa-solid fa-sitemap w-6"></i> Departments
                </a>
            </nav>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-1 p-8">

            <!-- 1. STAFF DASHBOARD -->
            <section id="screen-dashboard" class="">
                <header class="flex justify-between items-center mb-8">
                    <h2 class="text-3xl font-bold">Staff Overview</h2>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
                        <i class="fa-solid fa-plus mr-2"></i>Add Staff
                    </button>
                </header>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <p class="text-gray-500 text-sm uppercase font-semibold">Total Doctors</p>
                        <h3 class="text-3xl font-bold mt-1">42</h3>
                        <p class="text-green-500 text-sm mt-2"><i class="fa-solid fa-arrow-up"></i> 4 this month</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <p class="text-gray-500 text-sm uppercase font-semibold">Nurses on Duty</p>
                        <h3 class="text-3xl font-bold mt-1">118</h3>
                        <p class="text-blue-500 text-sm mt-2">Current Shift: Day</p>
                    </div>
                    <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                        <p class="text-gray-500 text-sm uppercase font-semibold">Avg. Response Time</p>
                        <h3 class="text-3xl font-bold mt-1">4.2m</h3>
                        <p class="text-orange-500 text-sm mt-2">Target: < 5.0m</p>
                    </div>
                </div>

                <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                    <table class="w-full text-left">
                        <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
                            <tr>
                                <th class="px-6 py-4">Name</th>
                                <th class="px-6 py-4">Specialty</th>
                                <th class="px-6 py-4">Department</th>
                                <th class="px-6 py-4">Status</th>
                                <th class="px-6 py-4">Action</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            <tr>
                                <td class="px-6 py-4 flex items-center">
                                    <div
                                        class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold mr-3">
                                        SH</div>
                                    <span class="font-medium">Dr. Sarah Higgins</span>
                                </td>
                                <td class="px-6 py-4">Cardiology</td>
                                <td class="px-6 py-4">Emergency Unit</td>
                                <td class="px-6 py-4">
                                    <span
                                        class="status-active px-3 py-1 rounded-full text-xs font-semibold">On-Duty</span>
                                </td>
                                <td class="px-6 py-4 text-blue-600 hover:underline cursor-pointer">View Details</td>
                            </tr>
                            <tr>
                                <td class="px-6 py-4 flex items-center">
                                    <div
                                        class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 font-bold mr-3">
                                        JM</div>
                                    <span class="font-medium">Nurse John Miller</span>
                                </td>
                                <td class="px-6 py-4">General Care</td>
                                <td class="px-6 py-4">Pediatrics</td>
                                <td class="px-6 py-4">
                                    <span
                                        class="status-on-call px-3 py-1 rounded-full text-xs font-semibold">On-Call</span>
                                </td>
                                <td class="px-6 py-4 text-blue-600 hover:underline cursor-pointer">View Details</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- 2. SHIFT SCHEDULING -->
            <section id="screen-scheduling" class="hidden">
                <header class="flex justify-between items-center mb-8">
                    <h2 class="text-3xl font-bold">Shift Scheduling</h2>
                    <div class="flex space-x-2">
                        <button class="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg">Week</button>
                        <button class="bg-blue-600 text-white px-4 py-2 rounded-lg">Month</button>
                    </div>
                </header>

                <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 overflow-x-auto">
                    <div class="grid grid-cols-8 gap-4 min-w-[800px]">
                        <div class="font-bold text-gray-400">Staff Member</div>
                        <div class="text-center font-bold">Mon 12</div>
                        <div class="text-center font-bold">Tue 13</div>
                        <div class="text-center font-bold">Wed 14</div>
                        <div class="text-center font-bold text-blue-600">Thu 15</div>
                        <div class="text-center font-bold">Fri 16</div>
                        <div class="text-center font-bold">Sat 17</div>
                        <div class="text-center font-bold">Sun 18</div>

                        <!-- Row 1 -->
                        <div class="py-4 font-medium text-sm">Dr. Sarah Higgins</div>
                        <div class="bg-blue-50 p-2 rounded text-xs text-blue-700 border border-blue-100 text-center">Day
                            Shift</div>
                        <div class="bg-blue-50 p-2 rounded text-xs text-blue-700 border border-blue-100 text-center">Day
                            Shift</div>
                        <div class="text-center text-gray-300">—</div>
                        <div
                            class="bg-indigo-50 p-2 rounded text-xs text-indigo-700 border border-indigo-100 text-center">
                            Night Shift</div>
                        <div
                            class="bg-indigo-50 p-2 rounded text-xs text-indigo-700 border border-indigo-100 text-center">
                            Night Shift</div>
                        <div class="text-center text-gray-300">—</div>
                        <div class="text-center text-gray-300">—</div>

                        <!-- Row 2 -->
                        <div class="py-4 font-medium text-sm">Nurse John Miller</div>
                        <div class="text-center text-gray-300">—</div>
                        <div class="bg-blue-50 p-2 rounded text-xs text-blue-700 border border-blue-100 text-center">Day
                            Shift</div>
                        <div class="bg-blue-50 p-2 rounded text-xs text-blue-700 border border-blue-100 text-center">Day
                            Shift</div>
                        <div class="bg-blue-50 p-2 rounded text-xs text-blue-700 border border-blue-100 text-center">Day
                            Shift</div>
                        <div class="text-center text-gray-300">—</div>
                        <div
                            class="bg-orange-50 p-2 rounded text-xs text-orange-700 border border-orange-100 text-center">
                            On-Call</div>
                        <div
                            class="bg-orange-50 p-2 rounded text-xs text-orange-700 border border-orange-100 text-center">
                            On-Call</div>
                    </div>
                </div>
            </section>

            <!-- 3. DEPARTMENT MANAGEMENT -->
            <section id="screen-departments" class="hidden">
                <header class="mb-8">
                    <h2 class="text-3xl font-bold">Department Management</h2>
                    <p class="text-gray-500">Overview of hospital units and resource allocation.</p>
                </header>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <!-- Dept Card 1 -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                        <div class="flex justify-between items-start mb-4">
                            <div class="p-3 bg-blue-100 text-blue-600 rounded-lg">
                                <i class="fa-solid fa-heart-pulse fa-xl"></i>
                            </div>
                            <span
                                class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase tracking-tight">Active</span>
                        </div>
                        <h4 class="text-xl font-bold">Cardiology</h4>
                        <p class="text-sm text-gray-500 mb-4">Focus on cardiac health and surgery.</p>
                        <div class="flex justify-between text-sm py-2 border-t border-gray-50">
                            <span>Head of Dept</span>
                            <span class="font-semibold">Dr. L. Banks</span>
                        </div>
                        <div class="flex justify-between text-sm py-2">
                            <span>Total Staff</span>
                            <span class="font-semibold">12</span>
                        </div>
                        <button
                            class="w-full mt-4 text-blue-600 bg-blue-50 py-2 rounded-lg font-semibold hover:bg-blue-100">Manage
                            Units</button>
                    </div>

                    <!-- Dept Card 2 -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                        <div class="flex justify-between items-start mb-4">
                            <div class="p-3 bg-red-100 text-red-600 rounded-lg">
                                <i class="fa-solid fa-truck-medical fa-xl"></i>
                            </div>
                            <span
                                class="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-bold uppercase">High
                                Load</span>
                        </div>
                        <h4 class="text-xl font-bold">Emergency (ER)</h4>
                        <p class="text-sm text-gray-500 mb-4">Critical care and 24/7 emergency response.</p>
                        <div class="flex justify-between text-sm py-2 border-t border-gray-50">
                            <span>Head of Dept</span>
                            <span class="font-semibold">Dr. A. Chen</span>
                        </div>
                        <div class="flex justify-between text-sm py-2">
                            <span>Total Staff</span>
                            <span class="font-semibold">24</span>
                        </div>
                        <button
                            class="w-full mt-4 text-blue-600 bg-blue-50 py-2 rounded-lg font-semibold hover:bg-blue-100">Manage
                            Units</button>
                    </div>

                    <!-- Dept Card 3 -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                        <div class="flex justify-between items-start mb-4">
                            <div class="p-3 bg-purple-100 text-purple-600 rounded-lg">
                                <i class="fa-solid fa-baby fa-xl"></i>
                            </div>
                            <span
                                class="bg-green-100 text-green-700 px-2 py-1 rounded text-xs font-bold uppercase tracking-tight">Active</span>
                        </div>
                        <h4 class="text-xl font-bold">Pediatrics</h4>
                        <p class="text-sm text-gray-500 mb-4">Healthcare for infants and children.</p>
                        <div class="flex justify-between text-sm py-2 border-t border-gray-50">
                            <span>Head of Dept</span>
                            <span class="font-semibold">Dr. S. Higgins</span>
                        </div>
                        <div class="flex justify-between text-sm py-2">
                            <span>Total Staff</span>
                            <span class="font-semibold">15</span>
                        </div>
                        <button
                            class="w-full mt-4 text-blue-600 bg-blue-50 py-2 rounded-lg font-semibold hover:bg-blue-100">Manage
                            Units</button>
                    </div>
                </div>
            </section>

        </main>
    </div>

    <!-- Simple Navigation JS -->
    <script>
        function showScreen(screenName) {
            // Hide all screens
            document.querySelectorAll('section').forEach(s => s.classList.add('hidden'));
            // Remove active classes from nav
            document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));

            // Show requested screen
            document.getElementById('screen-' + screenName).classList.remove('hidden');
            // Set nav item as active
            document.getElementById('nav-' + screenName).classList.add('active');
        }
    </script>
</body>

</html>
```
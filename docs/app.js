import { sportsData, rankings } from './data.js';

// DOM Elements
const desktopNav = document.getElementById('desktop-nav');
const mobileNavItems = document.getElementById('mobile-nav-items');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuIcon = mobileMenuBtn.querySelector('i');
const sportView = document.getElementById('sport-view');
const desktopRankings = document.getElementById('desktop-rankings');
const mobileRankings = document.getElementById('mobile-rankings');
const yearSpan = document.getElementById('year');

// State
let activeTab = sportsData && sportsData.length > 0 ? sportsData[0].id : null;
let isMobileMenuOpen = false;

// Initialization
function init() {
  if (!sportsData || !rankings) {
    throw new Error("Data failed to load. Check data.js file.");
  }

  yearSpan.textContent = new Date().getFullYear();
  renderNav();
  renderRankings();
  
  if (activeTab) {
    renderSport(activeTab);
  }
  
  // Event Listeners
  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', toggleMobileMenu);
  }

  // Initialize Icons safely
  updateIcons();
}

function updateIcons() {
  // Check if lucide is available globally (from CDN)
  // @ts-ignore
  if (typeof window.lucide !== 'undefined' && window.lucide.createIcons) {
    // @ts-ignore
    window.lucide.createIcons();
  }
}

// Navigation Rendering
function renderNav() {
  const navHtml = sportsData.map(sport => `
    <button
      data-id="${sport.id}"
      class="px-4 py-2 rounded-md text-sm font-medium transition-colors duration-150 whitespace-nowrap
      ${activeTab === sport.id 
        ? 'bg-white text-blue-900 shadow-sm' 
        : 'text-blue-100 hover:bg-blue-800 hover:text-white'
      }"
    >
      ${sport.name}
    </button>
  `).join('');

  if (desktopNav) desktopNav.innerHTML = navHtml;

  const mobileHtml = sportsData.map(sport => `
    <button
      data-id="${sport.id}"
      class="px-3 py-2 rounded-md text-sm font-medium text-left transition-colors
      ${activeTab === sport.id 
        ? 'bg-white text-blue-900' 
        : 'text-blue-100 hover:bg-blue-700'
      }"
    >
      ${sport.name}
    </button>
  `).join('');

  if (mobileNavItems) mobileNavItems.innerHTML = mobileHtml;

  // Attach click listeners
  const buttons = document.querySelectorAll('button[data-id]');
  buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // @ts-ignore
      activeTab = e.currentTarget.dataset.id;
      renderNav(); // Re-render to update active state
      renderSport(activeTab);
      if (isMobileMenuOpen) toggleMobileMenu();
    });
  });
}

function toggleMobileMenu() {
  isMobileMenuOpen = !isMobileMenuOpen;
  if (isMobileMenuOpen) {
    mobileMenu.classList.remove('hidden');
    mobileMenuIcon.setAttribute('data-lucide', 'x');
  } else {
    mobileMenu.classList.add('hidden');
    mobileMenuIcon.setAttribute('data-lucide', 'menu');
  }
  updateIcons();
}

// Rankings Rendering
function renderRankings() {
  const html = `
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center gap-2">
        <i data-lucide="trophy" class="w-5 h-5 text-yellow-600"></i>
        <h2 class="font-bold text-gray-800 uppercase tracking-wide text-sm">Power Rankings</h2>
      </div>
      <div class="divide-y divide-gray-100">
        ${rankings.map(sport => `
          <div class="p-4">
            <h3 class="font-bold text-gray-900 text-sm mb-2 uppercase">${sport.sport}</h3>
            <ol class="list-decimal list-inside space-y-1">
              ${sport.items.map(item => `
                <li class="text-gray-600 text-sm pl-1">
                  <span class="font-medium text-gray-900">${item.team}</span>
                </li>
              `).join('')}
            </ol>
          </div>
        `).join('')}
      </div>
    </div>
  `;
  
  if (desktopRankings) desktopRankings.innerHTML = html;
  if (mobileRankings) mobileRankings.innerHTML = html;
}

// Main Content Rendering
function renderSport(id) {
  const data = sportsData.find(d => d.id === id);
  if (!data || !sportView) return;

  let standingsHtml = '';
  if (data.standings.length > 0) {
    standingsHtml = `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        ${data.standings.map(group => `
          <div class="mb-8">
            <h3 class="text-lg font-bold text-gray-800 mb-3 uppercase border-b-2 border-blue-900 pb-1 inline-block">
              ${group.name}
            </h3>
            <div class="overflow-x-auto rounded-lg border border-gray-200">
              <table class="w-full text-sm text-left text-gray-600">
                <thead class="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th scope="col" class="px-4 py-3 font-bold w-1/3">Team</th>
                    ${group.headers.map(h => `<th scope="col" class="px-4 py-3 font-bold text-center">${h}</th>`).join('')}
                  </tr>
                </thead>
                <tbody>
                  ${group.rows.map((row, idx) => `
                    <tr class="border-b border-gray-100 last:border-0 hover:bg-gray-50 ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50/30'}">
                      <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap">${row.team}</th>
                      ${group.headers.map(h => `
                        <td class="px-4 py-3 text-center font-mono text-gray-700">
                          ${row[h.toLowerCase()] !== undefined ? row[h.toLowerCase()] : '-'}
                        </td>
                      `).join('')}
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  let leadersHtml = '';
  if (data.leaders.length > 0) {
    leadersHtml = `
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <h3 class="text-xl font-bold text-gray-900 mb-6 uppercase border-b border-gray-200 pb-2">
          Individual Leaders
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-8">
          ${data.leaders.map(cat => `
            <div class="mb-8 break-inside-avoid">
              <h3 class="text-md font-bold text-gray-700 mb-3 bg-gray-100 px-2 py-1 uppercase tracking-wider inline-block rounded text-xs">
                ${cat.categoryName}
              </h3>
              <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                  <thead class="text-xs text-gray-500 uppercase border-b border-gray-200">
                    <tr>
                      <th scope="col" class="px-2 py-2 font-semibold">Player, School</th>
                      ${cat.headers.map(h => `<th scope="col" class="px-2 py-2 font-semibold text-right">${h.label}</th>`).join('')}
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    ${cat.players.map(p => `
                      <tr class="hover:bg-gray-50">
                        <td class="px-2 py-2 font-medium text-gray-900">
                          <span class="block">${p.player}</span>
                          <span class="text-xs text-gray-500 font-normal">${p.school}</span>
                        </td>
                        ${cat.headers.map(h => `
                          <td class="px-2 py-2 text-right font-mono text-gray-700">${p[h.key]}</td>
                        `).join('')}
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  sportView.innerHTML = `
    <div class="mb-8">
      <h2 class="text-3xl font-extrabold text-gray-900 uppercase tracking-tight mb-6">
        ${data.name}
      </h2>
      ${standingsHtml}
      ${leadersHtml}
    </div>
  `;

  updateIcons();
}

// Start
document.addEventListener('DOMContentLoaded', init);
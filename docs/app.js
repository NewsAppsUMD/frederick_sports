import { sportsData, rankings, availableDates } from './data.js';

// DOM Elements
const navContainer = document.getElementById('nav-container');
const sportView = document.getElementById('sport-view');
const rankingsContainer = document.getElementById('rankings-container');
const dateSelector = document.getElementById('date-selector');

// State
let activeTab = null;
let selectedDate = availableDates && availableDates.length > 0 ? availableDates[availableDates.length - 1].value : null;

// Get filtered data for selected date
function getFilteredSportsData() {
  if (!sportsData || !selectedDate) return [];
  return sportsData.filter(sport => sport.date === selectedDate);
}

function getFilteredRankings() {
  if (!rankings || !selectedDate) return [];
  const dateRankings = rankings.find(r => r.date === selectedDate);
  return dateRankings ? dateRankings.items : [];
}

// Initialization
function init() {
  if (!sportsData || !rankings) {
    throw new Error("Data failed to load. Check data.js file.");
  }

  renderDateSelector();
  renderNav();
  renderRankings();

  const filteredData = getFilteredSportsData();
  if (filteredData.length > 0) {
    activeTab = filteredData[0].id;
    renderSport(activeTab);
  }
}

// Date Selector Rendering
function renderDateSelector() {
  if (!dateSelector || !availableDates) return;

  dateSelector.innerHTML = availableDates.map(date => `
    <option value="${date.value}" ${selectedDate === date.value ? 'selected' : ''}>
      ${date.label}
    </option>
  `).join('');

  dateSelector.addEventListener('change', (e) => {
    selectedDate = e.target.value;
    // Update header date display
    const dateDisplay = document.getElementById('date-display');
    const selectedDateObj = availableDates.find(d => d.value === selectedDate);
    if (dateDisplay && selectedDateObj) {
      dateDisplay.textContent = `Updated ${selectedDateObj.label}`;
    }
    // Re-render everything
    renderNav();
    renderRankings();
    const filteredData = getFilteredSportsData();
    if (filteredData.length > 0) {
      // Try to keep same sport selected, or default to first
      const currentSportExists = filteredData.some(s => s.id === activeTab);
      if (!currentSportExists) {
        activeTab = filteredData[0].id;
      }
      renderSport(activeTab);
    }
  });
}

// Navigation Rendering
function renderNav() {
  if (!navContainer) return;

  const filteredData = getFilteredSportsData();

  navContainer.innerHTML = filteredData.map(sport => `
    <button
      data-id="${sport.id}"
      class="px-4 py-2 rounded border text-sm font-semibold transition-colors
      ${activeTab === sport.id
        ? 'bg-blue-900 text-white border-blue-900'
        : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100 hover:border-gray-300'
      }"
    >
      ${sport.name}
    </button>
  `).join('');

  // Attach click listeners
  const buttons = document.querySelectorAll('button[data-id]');
  buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // @ts-ignore
      activeTab = e.currentTarget.dataset.id;
      renderNav(); // Re-render to update active state
      renderSport(activeTab);
    });
  });
}

// Rankings Rendering (Simplified for footer/grid layout)
function renderRankings() {
  if (!rankingsContainer) return;

  const filteredRankings = getFilteredRankings();

  rankingsContainer.innerHTML = filteredRankings.map(sport => `
    <div class="bg-gray-50 p-4 rounded border border-gray-200">
      <h3 class="font-bold text-gray-800 text-sm mb-3 uppercase border-b border-gray-200 pb-1">${sport.sport}</h3>
      <ol class="list-decimal list-inside space-y-1">
        ${sport.items.map(item => `
          <li class="text-gray-600 text-sm">
            <span class="font-medium text-gray-900">${item.team}</span>
          </li>
        `).join('')}
      </ol>
    </div>
  `).join('');
}

// Main Content Rendering
function renderSport(id) {
  const filteredData = getFilteredSportsData();
  const data = filteredData.find(d => d.id === id);
  if (!data || !sportView) return;

  let standingsHtml = '';
  if (data.standings && data.standings.length > 0) {
    standingsHtml = `
      <div class="mb-10">
        <h3 class="text-xl font-bold text-gray-800 mb-4">Standings</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          ${data.standings.map(group => `
            <div>
              <h4 class="font-bold text-gray-700 mb-2 uppercase text-sm tracking-wide">
                ${group.division}
              </h4>
              <div class="overflow-x-auto border border-gray-200 rounded">
                <table class="w-full text-sm text-left">
                  <thead class="bg-gray-100 text-gray-600 uppercase text-xs font-semibold">
                    <tr>
                      <th class="px-3 py-2 w-1/3">Team</th>
                      ${group.headers.map(h => `<th class="px-3 py-2 text-center">${h.label}</th>`).join('')}
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    ${group.teams.map((team, idx) => `
                      <tr class="${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}">
                        <td class="px-3 py-2 font-medium text-gray-900 whitespace-nowrap">${team.team}</td>
                        ${group.headers.map(h => `
                          <td class="px-3 py-2 text-center text-gray-700 font-mono">
                            ${team[h.key] !== undefined && team[h.key] !== '' ? team[h.key] : '-'}
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
      </div>
    `;
  }

  let leadersHtml = '';
  if (data.leaders.length > 0) {
    leadersHtml = `
      <div>
        <h3 class="text-xl font-bold text-gray-800 mb-4">Individual Leaders</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          ${data.leaders.map(cat => `
            <div class="border border-gray-200 rounded bg-white overflow-hidden">
              <div class="bg-gray-100 px-3 py-2 border-b border-gray-200">
                <h4 class="font-bold text-gray-700 text-xs uppercase tracking-wider">
                  ${cat.categoryName}
                </h4>
              </div>
              <div class="overflow-x-auto">
                <table class="w-full text-sm">
                  <thead class="text-xs text-gray-500 bg-gray-50 border-b border-gray-100">
                    <tr>
                      <th class="px-3 py-2 text-left font-semibold">Player</th>
                      ${cat.headers.map(h => `<th class="px-3 py-2 text-right font-semibold">${h.label}</th>`).join('')}
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    ${cat.players.map(p => `
                      <tr class="hover:bg-gray-50">
                        <td class="px-3 py-2">
                          <div class="font-medium text-gray-900">${p.player}</div>
                          <div class="text-xs text-gray-500">${p.school}</div>
                        </td>
                        ${cat.headers.map(h => `
                          <td class="px-3 py-2 text-right font-mono text-gray-700">${p[h.key]}</td>
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
    <div class="animate-in fade-in duration-300">
      <h2 class="text-2xl font-bold text-blue-900 mb-6 pb-2 border-b border-gray-200">
        ${data.name}
      </h2>
      ${standingsHtml}
      ${leadersHtml}
    </div>
  `;
}

// Start
document.addEventListener('DOMContentLoaded', init);

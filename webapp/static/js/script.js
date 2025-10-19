const teamsData = {
  laliga: [
    'Alavés','Athletic','Atlético','Barcelona','Betis','Celta','Espanyol',
    'Getafe','Girona','Las Palmas','Leganés','Mallorca','Osasuna',
    'R. Sociedad','Rayo','Real Madrid','Sevilla','Valencia','Valladolid','Villarreal'
  ],
  epl: [
    'Arsenal','Aston Villa','Bournemouth','Brentford','Brighton and Hove Albion',
    'Chelsea','Crystal Palace','Everton','Fulham','Ipswich Town','Leicester City',
    'Liverpool','M. City','M. United','Newcastle United','Nottingham Forest',
    'Southampton','Tottenham H.','West Ham Utd.','Wolverhampton Wanderers'
  ],
  seriea: ['Juventus', 'Inter Milan', 'AC Milan', 'Napoli', 'Roma'],
  ucl: [
    'Arsenal','Aston Villa','Atalanta','Atlético','Barcelona','Bayer 04 Leverkusen',
    'Bayern Múnich','Benfica','Bolonia','Borussia Dortmund','Brest','Brujas','Celtic',
    'Dinamo Zagreb','Estrella Roja','Feyenoord','Girona','Inter Milán','Juventus',
    'Leipzig','Lille','Liverpool','M. City','Milan','Monaco','PSG','PSV','Real Madrid',
    'Salzburgo','Shakhtar Donetsk','SK Puntigamer Sturm Graz','SK Slovan Bratislava',
    'Sp. Portugal','Sparta Praga','VfB Stuttgart','Young Boys'
  ]
};

// Dynamically show teams based on selected competitions
function updateTeams() {
  const selectedComps = Array.from(
    document.querySelectorAll('#competitionDropdown input:checked')
  ).map(i => i.value);

  const teamDropdown = document.getElementById('teamDropdown');
  teamDropdown.innerHTML = '';

  if (!selectedComps.length) {
    teamDropdown.innerHTML = '<p class="text-gray-400 italic">Choose a competition above to load teams.</p>';
    return;
  }

  const added = new Set();

  selectedComps.forEach(comp => {
    const teams = teamsData[comp]?.filter(t => !added.has(t)) || [];
    if (!teams.length) return;

    const heading = document.createElement('h4');
    heading.textContent = comp.toUpperCase();
    heading.className = 'font-semibold text-emerald-400 mt-3 mb-2';
    teamDropdown.appendChild(heading);

    const container = document.createElement('div');
    container.className = 'grid grid-cols-2 gap-2 mb-3';

    teams.forEach(team => {
      added.add(team);
      const label = document.createElement('label');
      label.className = 'flex items-center gap-2 bg-white bg-opacity-10 px-2 py-1 rounded hover:bg-opacity-20 transition';

      const input = document.createElement('input');
      input.type = 'checkbox';
      input.name = 'team[]';
      input.value = team;
      input.className = 'accent-emerald-500';

      label.appendChild(input);
      label.appendChild(document.createTextNode(team));
      container.appendChild(label);
    });

    teamDropdown.appendChild(container);
  });
}

// Handle form submission (generate subscription link)
const form = document.getElementById('uploadForm');
form.addEventListener('submit', async e => {
  e.preventDefault();

  const formData = new FormData(form);
  const response = await fetch('/generate', { method: 'POST', body: formData });
  if (!response.ok) {
    alert('Error generating calendar. Please try again.');
    return;
  }

  const { ics_url } = await response.json();
  showSubscriptionSection(ics_url);
});

// Show subscription + download links
function showSubscriptionSection(icsUrl) {
  const form = document.getElementById('uploadForm');
  const section = document.getElementById('subscriptionSection');

  // hide form and show subscription section
  form.classList.add('hidden');
  section.classList.remove('hidden');

  // fill in links
  document.getElementById('subscriptionLink').value = icsUrl;
  document.getElementById('downloadLink').href = icsUrl;
  document.getElementById('googleCalendarBtn').href =
    `https://calendar.google.com/calendar/u/0/r?cid=${encodeURIComponent(icsUrl)}`;
  document.getElementById('appleCalendarBtn').href = icsUrl;
}

// Copy subscription URL
function copySubscriptionLink() {
  const input = document.getElementById('subscriptionLink');
  navigator.clipboard.writeText(input.value).then(() =>
    alert('✅ Subscription link copied!')
  );
}

function resetForm() {
  window.location.href = "/";
}
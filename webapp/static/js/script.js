const teamsData = {
	laliga: [
		'Alav\u00e9s',
		'Athletic',
		'Atl\u00e9tico',
		'Barcelona',
		'Betis',
		'Celta',
		'Espanyol',
		'Getafe',
		'Girona',
		'Las Palmas',
		'Legan\u00e9s',
		'Mallorca',
		'Osasuna',
		'R. Sociedad',
		'Rayo',
		'Real Madrid',
		'Sevilla',
		'Valencia',
		'Valladolid',
		'Villarreal',
	],
	epl: [
		'Arsenal',
		'Aston Villa',
		'Bournemouth',
		'Brentford',
		'Brighton and Hove Albion',
		'Chelsea',
		'Crystal Palace',
		'Everton',
		'Fulham',
		'Ipswich Town',
		'Leicester City',
		'Liverpool',
		'M. City',
		'M. United',
		'Newcastle United',
		'Nottingham Forest',
		'Southampton',
		'Tottenham H.',
		'West Ham Utd.',
		'Wolverhampton Wanderers',
	],
	seriea: ['Juventus', 'Inter Milan', 'AC Milan', 'Napoli', 'Roma'],
};

function updateTeams() {
	const selectedCompetitions = Array.from(
		document.querySelectorAll('#competitionDropdown input:checked')
	).map((input) => input.value);

	const teamDropdown = document.getElementById('teamDropdown');
	teamDropdown.innerHTML = ''; // Clear existing teams

	selectedCompetitions.forEach((competition) => {
		if (teamsData[competition]) {
			teamsData[competition].forEach((team) => {
				const label = document.createElement('label');
				const input = document.createElement('input');
				input.type = 'checkbox';
				input.value = team.replace(/\s+/g, '');
				input.id = team.replace(/\s+/g, '');
				input.name = 'team'
				label.appendChild(input);
				label.appendChild(document.createTextNode(' ' + team));
				teamDropdown.appendChild(label);
			});
		}
	});
}

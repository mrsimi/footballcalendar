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
	ucl: [
		"Arsenal",
		"Aston Villa",
		"Atalanta",
		"Atl\u00e9tico",
		"Barcelona",
		"Bayer 04 Leverkusen",
		"Bayern M\u00fanich",
		"Benfica",
		"Bolonia",
		"Borussia Dortmund",
		"Brest",
		"Brujas",
		"Celtic",
		"Dinamo Zagreb",
		"Estrella Roja",
		"Feyenoord",
		"Girona",
		"Inter Mil\u00e1n",
		"Juventus",
		"Leipzig",
		"Lille",
		"Liverpool",
		"M. City",
		"Milan",
		"Monaco",
		"PSG",
		"PSV",
		"Real Madrid",
		"Salzburgo",
		"Shakhtar Donetsk",
		"SK Puntigamer Sturm Graz",
		"SK Slovan Bratislava",
		"Sp. Portugal",
		"Sparta Praga",
		"VfB Stuttgart",
		"Young Boys"
	]	
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
				input.value = team;
				input.id = team;
				input.name = 'team'
				label.appendChild(input);
				label.appendChild(document.createTextNode(' ' + team));
				teamDropdown.appendChild(label);
			});
		}
	});
}

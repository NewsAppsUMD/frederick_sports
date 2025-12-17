export const rankings = [
  {
    sport: 'Football',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Oakdale' },
      { rank: 3, team: 'Middletown' },
      { rank: 4, team: 'Urbana' },
    ]
  },
  {
    sport: 'Boys Soccer',
    items: [
      { rank: 1, team: 'Tuscarora' },
      { rank: 2, team: 'Urbana' },
      { rank: 3, team: 'Linganore' },
      { rank: 4, team: 'Brunswick' },
    ]
  },
  {
    sport: 'Girls Flag Football',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Linganore' },
      { rank: 3, team: 'Frederick' },
      { rank: 4, team: 'Thomas Johnson' },
    ]
  },
  {
    sport: 'Girls Soccer',
    items: [
      { rank: 1, team: 'Oakdale' },
      { rank: 2, team: 'Linganore' },
      { rank: 3, team: 'Brunswick' },
      { rank: 4, team: 'Middletown' },
    ]
  },
  {
    sport: 'Volleyball',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Tuscarora' },
      { rank: 3, team: 'Oakdale' },
      { rank: 4, team: 'Maryland School for the Deaf' },
    ]
  },
  {
    sport: 'Field Hockey',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Urbana' },
      { rank: 3, team: 'Walkersville' },
      { rank: 4, team: 'Oakdale' },
    ]
  },
  {
    sport: 'Boys Cross Country',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Thomas Johnson' },
      { rank: 3, team: 'Brunswick' },
      { rank: 4, team: 'Oakdale' },
    ]
  },
  {
    sport: 'Girls Cross Country',
    items: [
      { rank: 1, team: 'Urbana' },
      { rank: 2, team: 'Thomas Johnson' },
      { rank: 3, team: 'Frederick' },
      { rank: 4, team: 'Tuscarora' },
    ]
  },
  {
    sport: 'Golf',
    items: [
      { rank: 1, team: 'Linganore' },
      { rank: 2, team: 'Middletown' },
      { rank: 3, team: 'Oakdale' },
    ]
  },
];

export const sportsData = [
  {
    id: 'football',
    name: 'Football',
    standings: [
      {
        name: 'FCPS',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Linganore', w: 13, l: 0, pf: 578, pa: 137 },
          { team: 'Oakdale', w: 10, l: 3, pf: 478, pa: 221 },
          { team: 'Middletown', w: 8, l: 3, pf: 371, pa: 150 },
          { team: 'Urbana', w: 7, l: 5, pf: 348, pa: 234 },
          { team: 'Walkersville', w: 7, l: 5, pf: 377, pa: 292 },
          { team: 'Frederick', w: 5, l: 6, pf: 318, pa: 283 },
          { team: 'Brunswick', w: 2, l: 8, pf: 152, pa: 334 },
          { team: 'Thomas Johnson', w: 2, l: 8, pf: 213, pa: 442 },
          { team: 'Tuscarora', w: 2, l: 8, pf: 154, pa: 425 },
          { team: 'Catoctin', w: 1, l: 9, pf: 72, pa: 301 },
        ]
      },
      {
        name: 'Other Schools',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Maryland School for the Deaf', w: 9, l: 3, pf: 418, pa: 127 },
          { team: "St. John's Catholic Prep", w: 0, l: 10, pf: 92, pa: 333 },
        ]
      }
    ],
    leaders: [
      {
        categoryName: 'Rushing',
        headers: [
            { key: 'att', label: 'Att' }, 
            { key: 'yds', label: 'Yds' }, 
            { key: 'avg', label: 'Avg' }, 
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Bradly Matthews', school: 'Linganore', att: 246, yds: '2,124', avg: 8.63, td: 41 },
          { player: 'Colton Amoriell', school: 'Walkersville', att: 235, yds: '1,765', avg: 7.5, td: 21 },
          { player: 'Mark Gwynn III', school: 'Maryland School for the Deaf', att: 103, yds: '1,095', avg: 10.63, td: 14 },
          { player: 'Alex Rodriguez', school: 'Oakdale', att: 134, yds: '1,042', avg: 7.77, td: 16 },
          { player: 'Nakhi Bagwell', school: 'Thomas Johnson', att: 159, yds: 892, avg: 5.61, td: 5 },
          { player: 'Shemiah Hill', school: 'Oakdale', att: 104, yds: 820, avg: 7.88, td: 8 },
          { player: 'Owen Brooks', school: 'Walkersville', att: 100, yds: 764, avg: 7.6, td: 15 },
          { player: 'Ryan McLister', school: 'Middletown', att: 66, yds: 618, avg: 9.36, td: 9 },
          { player: 'Miles Robinson', school: 'Frederick', att: 93, yds: 554, avg: 6, td: 8 },
          { player: 'Ryker Pedersen', school: 'Maryland School for the Deaf', att: 85, yds: 542, avg: 6.3, td: 10 },
        ]
      },
      {
        categoryName: 'Passing',
        headers: [
            { key: 'comp', label: 'Comp' }, 
            { key: 'att', label: 'Att' }, 
            { key: 'pct', label: 'Pct' }, 
            { key: 'yds', label: 'Yds' },
            { key: 'td', label: 'TD' }
        ],
        players: [
          { player: 'Brittin Poffenbarger', school: 'Middletown', comp: 148, att: 206, pct: '.718', yds: '2,461', td: 29 },
          { player: 'Randy Embrey', school: 'Thomas Johnson', comp: 145, att: 265, pct: '.547', yds: '2,243', td: 22 },
          { player: 'Miles Robinson', school: 'Frederick', comp: 197, att: 282, pct: '.699', yds: '2,096', td: 16 },
          { player: 'David Doy', school: 'Linganore', comp: 117, att: 172, pct: '.680', yds: '1,996', td: 28 },
          { player: 'Alex Rodriguez', school: 'Oakdale', comp: 112, att: 205, pct: '.546', yds: '1,762', td: 19 },
          { player: 'Landon Rosenberg', school: 'Tuscarora', comp: 108, att: 209, pct: '.517', yds: '1,280', td: 10 }
        ]
      }
    ]
  },
  {
    id: 'girls-flag-football',
    name: 'Girls Flag Football',
    standings: [
      {
        name: 'FCPS',
        headers: ['W', 'L', 'PF', 'PA'],
        rows: [
          { team: 'Urbana', w: 12, l: 1, pf: 380, pa: 100 },
          { team: 'Linganore', w: 13, l: 3, pf: 400, pa: 127 },
          { team: 'Frederick', w: 9, l: 4, pf: 250, pa: 180 },
          { team: 'Thomas Johnson', w: 7, l: 6, pf: 200, pa: 210 },
          { team: 'Middletown', w: 6, l: 7, pf: 180, pa: 200 },
          { team: 'Oakdale', w: 5, l: 8, pf: 150, pa: 250 },
          { team: 'Walkersville', w: 4, l: 9, pf: 120, pa: 280 },
          { team: 'Tuscarora', w: 2, l: 11, pf: 90, pa: 320 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'boys-soccer',
    name: 'Boys Soccer',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Tuscarora', w: 14, l: 2, t: 1 },
          { team: 'Urbana', w: 13, l: 3, t: 1 },
          { team: 'Linganore', w: 11, l: 4, t: 2 },
          { team: 'Brunswick', w: 10, l: 5, t: 3 },
          { team: 'Middletown', w: 9, l: 6, t: 1 },
          { team: 'Oakdale', w: 8, l: 7, t: 2 },
          { team: 'Frederick', w: 6, l: 9, t: 1 },
          { team: 'Thomas Johnson', w: 5, l: 10, t: 0 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'girls-soccer',
    name: 'Girls Soccer',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Oakdale', w: 15, l: 1, t: 1 },
          { team: 'Linganore', w: 13, l: 3, t: 1 },
          { team: 'Brunswick', w: 12, l: 4, t: 0 },
          { team: 'Middletown', w: 10, l: 5, t: 2 },
          { team: 'Urbana', w: 9, l: 6, t: 1 },
          { team: 'Walkersville', w: 7, l: 8, t: 1 },
          { team: 'Tuscarora', w: 5, l: 10, t: 2 },
          { team: 'Frederick', w: 4, l: 11, t: 0 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'volleyball',
    name: 'Volleyball',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L'],
        rows: [
          { team: 'Urbana', w: 18, l: 2 },
          { team: 'Tuscarora', w: 16, l: 4 },
          { team: 'Oakdale', w: 14, l: 5 },
          { team: 'MSD', w: 12, l: 6 },
          { team: 'Linganore', w: 10, l: 8 },
          { team: 'Middletown', w: 9, l: 9 },
          { team: 'Frederick', w: 6, l: 12 },
        ]
      }
    ],
    leaders: []
  },
  {
    id: 'field-hockey',
    name: 'Field Hockey',
    standings: [
      {
        name: 'Standings',
        headers: ['W', 'L', 'T'],
        rows: [
          { team: 'Linganore', w: 14, l: 2, t: 0 },
          { team: 'Urbana', w: 13, l: 3, t: 1 },
          { team: 'Walkersville', w: 11, l: 5, t: 0 },
          { team: 'Oakdale', w: 10, l: 6, t: 1 },
          { team: 'Middletown', w: 8, l: 7, t: 2 },
          { team: 'Frederick', w: 5, l: 10, t: 0 },
        ]
      }
    ],
    leaders: []
  }
];
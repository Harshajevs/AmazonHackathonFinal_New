
import { Movie } from '../types/Movie';

export const movieData: Movie[] = [
  // Trending Movies
  {
    id: '1',
    title: 'Avatar: The Way of Water',
    description: 'Jake Sully and Neytiri have formed a family and are doing everything to stay together. However, they must leave their home and explore the regions of Pandora.',
    genre: ['Sci-Fi', 'Action', 'Adventure'],
    duration: '3h 12m',
    rating: '7.6',
    year: 2022,
    image: '/images/image1.png',
    platform: 'Hotstar',
    featured: true
  },
  {
    id: '2',
    title: 'Stranger Things 4',
    description: 'It\'s been six months since the Battle of Starcourt, which brought terror and destruction to Hawkins. Struggling with the aftermath, our group of friends are separated for the first time.',
    genre: ['Drama', 'Horror', 'Sci-Fi'],
    duration: '1h 20m',
    rating: '8.7',
    year: 2022,
    image: '/images/image2.png',
    platform: 'Netflix'
  },
  {
    id: '3',
    title: 'The Lord of the Rings: The Rings of Power',
    description: 'Epic drama set thousands of years before the events of J.R.R. Tolkien\'s The Hobbit and The Lord of the Rings follows an ensemble cast of characters.',
    genre: ['Fantasy', 'Adventure', 'Drama'],
    duration: '1h 10m',
    rating: '6.9',
    year: 2022,
    image: '/images/image3.png',
    platform: 'Prime Video'
  },
  {
    id: '4',
    title: 'RRR',
    description: 'A fictitious story about two legendary revolutionaries and their journey away from home before they started fighting for their country in 1920s.',
    genre: ['Action', 'Drama'],
    duration: '3h 7m',
    rating: '7.9',
    year: 2022,
    image: '/images/image4.png',
    platform: 'Aha'
  },
  {
    id: '5',
    title: 'House of the Dragon',
    description: 'The story of the Targaryen civil war that took place about 300 years before events portrayed in Game of Thrones.',
    genre: ['Drama', 'Fantasy', 'Action'],
    duration: '1h 6m',
    rating: '8.5',
    year: 2022,
    image: '/images/image5.png',
    platform: 'Hotstar'
  },
  {
    id: '6',
    title: 'Wednesday',
    description: 'Smart, sarcastic and a little dead inside, Wednesday Addams investigates a murder spree while making new friends — and foes — at Nevermore Academy.',
    genre: ['Comedy', 'Crime', 'Family'],
    duration: '50m',
    rating: '8.1',
    year: 2022,
    image: '/images/image6.png',
    platform: 'Netflix'
  },
  {
    id: '7',
    title: 'Top Gun: Maverick',
    description: 'After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN\'s elite graduates on a mission.',
    genre: ['Action', 'Drama'],
    duration: '2h 10m',
    rating: '8.3',
    year: 2022,
    image: '/images/image7.png',
    platform: 'Prime Video'
  },
  {
    id: '8',
    title: 'The Boys',
    description: 'A group of vigilantes set out to take down corrupt superheroes who abuse their superpowers.',
    genre: ['Action', 'Comedy', 'Crime'],
    duration: '1h',
    rating: '8.7',
    year: 2022,
    image: '/images/image8.png',
    platform: 'Prime Video'
  },
  {
    id: '9',
    title: 'Euphoria',
    description: 'A look at life for a group of high school students as they grapple with issues of drugs, sex, and violence.',
    genre: ['Drama'],
    duration: '1h',
    rating: '8.4',
    year: 2022,
    image: '/images/image9.png',
    platform: 'Hotstar'
  },
  {
    id: '10',
    title: 'Money Heist',
    description: 'An unusual group of robbers attempt to carry out the most perfect robbery in Spanish history - stealing 2.4 billion euros from the Royal Mint of Spain.',
    genre: ['Action', 'Crime', 'Mystery'],
    duration: '1h 10m',
    rating: '8.2',
    year: 2021,
    image: '/images/image10.png',
    platform: 'Netflix'
  },
  {
    id: '11',
    title: 'Pushpa: The Rise',
    description: 'A laborer named Pushpa makes enemies as he rises in the world of red sandalwood smuggling. However, violence erupts when the police attempt to bring down his illegal business.',
    genre: ['Action', 'Crime', 'Drama'],
    duration: '2h 59m',
    rating: '7.6',
    year: 2021,
    image: '/images/image11.png',
    platform: 'Aha'
  },
  {
    id: '12',
    title: 'Dune',
    description: 'Feature adaptation of Frank Herbert\'s science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset.',
    genre: ['Action', 'Adventure', 'Drama'],
    duration: '2h 35m',
    rating: '8.0',
    year: 2021,
    image: '/images/image12.png',
    platform: 'Prime Video'
  },
  {
    id: '13',
    title: 'Squid Game',
    description: 'Hundreds of cash-strapped players accept a strange invitation to compete in children\'s games for a tempting prize, but the stakes are deadly.',
    genre: ['Action', 'Drama', 'Mystery'],
    duration: '1h',
    rating: '8.0',
    year: 2021,
    image: '/images/image13.png',
    platform: 'Netflix'
  },
  {
    id: '14',
    title: 'Loki',
    description: 'The mercurial villain Loki resumes his role as the God of Mischief following the events of Avengers: Endgame.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '50m',
    rating: '8.2',
    year: 2021,
    image: '/images/image14.png',
    platform: 'Hotstar'
  },
  {
    id: '15',
    title: 'Arya 2',
    description: 'Arya, an unconventional young man, falls in love with Geetha at first sight. He tries to impress her in various ways but fails.',
    genre: ['Comedy', 'Drama', 'Romance'],
    duration: '2h 35m',
    rating: '7.8',
    year: 2009,
    image: '/images/image15.png',
    platform: 'Aha'
  },
  // Adding 30 more movies
  {
    id: '16',
    title: 'Black Panther: Wakanda Forever',
    description: 'The people of Wakanda fight to protect their home from intervening world powers as they mourn the death of King T\'Challa.',
    genre: ['Action', 'Adventure', 'Drama'],
    duration: '2h 41m',
    rating: '6.7',
    year: 2022,
    image: '/images/image16.png',
    platform: 'Hotstar'
  },
  {
    id: '17',
    title: 'The Batman',
    description: 'When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city\'s hidden corruption.',
    genre: ['Action', 'Crime', 'Drama'],
    duration: '2h 56m',
    rating: '7.8',
    year: 2022,
    image: '/images/image17.png',
    platform: 'Prime Video'
  },
  {
    id: '18',
    title: 'Ozark',
    description: 'A financial advisor drags his family from Chicago to the Missouri Ozarks, where he launders money to appease a drug boss.',
    genre: ['Crime', 'Drama', 'Thriller'],
    duration: '1h',
    rating: '8.4',
    year: 2022,
    image: '/images/image18.png',
    platform: 'Netflix'
  },
  {
    id: '19',
    title: 'The Witcher',
    description: 'Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world where people often prove more wicked than beasts.',
    genre: ['Action', 'Adventure', 'Drama'],
    duration: '1h',
    rating: '8.2',
    year: 2021,
    image: '/images/image19.png',
    platform: 'Netflix'
  },
  {
    id: '20',
    title: 'Spider-Man: No Way Home',
    description: 'With Spider-Man\'s identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds start to appear.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '2h 28m',
    rating: '8.2',
    year: 2021,
    image: '/images/image20.png',
    platform: 'Prime Video'
  },
  {
    id: '21',
    title: 'Encanto',
    description: 'A Colombian teenage girl has to face the frustration of being the only member of her family without magical powers.',
    genre: ['Animation', 'Comedy', 'Family'],
    duration: '1h 42m',
    rating: '7.2',
    year: 2021,
    image: '/images/image21.png',
    platform: 'Hotstar'
  },
  {
    id: '22',
    title: 'The Mandalorian',
    description: 'The travels of a lone bounty hunter in the outer reaches of the galaxy, far from the authority of the New Republic.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '40m',
    rating: '8.7',
    year: 2020,
    image: '/images/image22.png',
    platform: 'Hotstar'
  },
  {
    id: '23',
    title: 'Eternals',
    description: 'The saga of the Eternals, a race of immortal beings who lived on Earth and shaped its history and civilizations.',
    genre: ['Action', 'Adventure', 'Drama'],
    duration: '2h 36m',
    rating: '6.3',
    year: 2021,
    image: '/images/image23.png',
    platform: 'Hotstar'
  },
  {
    id: '24',
    title: 'Fast & Furious 9',
    description: 'Dom and the crew must take on an international terrorist who turns out to be Dom and Mia\'s estranged brother.',
    genre: ['Action', 'Crime', 'Thriller'],
    duration: '2h 23m',
    rating: '5.2',
    year: 2021,
    image: '/images/image24.png',
    platform: 'Prime Video'
  },
  {
    id: '25',
    title: 'Cruella',
    description: 'A live-action prequel feature film following a young Cruella de Vil.',
    genre: ['Comedy', 'Crime', 'Drama'],
    duration: '2h 14m',
    rating: '7.3',
    year: 2021,
    image: '/images/image25.png',
    platform: 'Hotstar'
  },
  {
    id: '26',
    title: 'Wonder Woman 1984',
    description: 'Diana must contend with a work colleague and businessman, whose desire for extreme wealth sends the world down a path of destruction.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '2h 31m',
    rating: '5.4',
    year: 2020,
    image: '/images/image26.jpg',
    platform: 'Prime Video'
  },
  {
    id: '27',
    title: 'Black Widow',
    description: 'Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.',
    genre: ['Action', 'Adventure', 'Sci-Fi'],
    duration: '2h 14m',
    rating: '6.7',
    year: 2021,
    image: '/images/image27.jpg',
    platform: 'Hotstar'
  },
  {
    id: '28',
    title: 'Shang-Chi and the Legend of the Ten Rings',
    description: 'Shang-Chi must confront the past he thought he left behind when he is drawn into the web of the mysterious Ten Rings organization.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '2h 12m',
    rating: '7.4',
    year: 2021,
    image: '/images/image28.jpg',
    platform: 'Hotstar'
  },
  {
    id: '29',
    title: 'Free Guy',
    description: 'A bank teller discovers that he\'s actually an NPC inside a brutal, open world video game.',
    genre: ['Action', 'Adventure', 'Comedy'],
    duration: '1h 55m',
    rating: '7.1',
    year: 2021,
    image: '/images/image29.jpg',
    platform: 'Prime Video'
  },
  {
    id: '30',
    title: 'The Suicide Squad',
    description: 'Supervillains Harley Quinn, Bloodsport, Peacemaker and a collection of nutty cons at Belle Reve prison join the super-secret, super-shady Task Force X.',
    genre: ['Action', 'Adventure', 'Comedy'],
    duration: '2h 12m',
    rating: '7.2',
    year: 2021,
    image: '/images/image30.jpg',
    platform: 'Prime Video'
  },
  {
    id: '31',
    title: 'Jungle Cruise',
    description: 'Based on Disneyland\'s theme park ride where a small riverboat takes a group of travelers through a jungle filled with dangerous animals and reptiles.',
    genre: ['Action', 'Adventure', 'Comedy'],
    duration: '2h 7m',
    rating: '6.6',
    year: 2021,
    image: '/images/image31.jpg',
    platform: 'Hotstar'
  },
  {
    id: '32',
    title: 'No Time to Die',
    description: 'James Bond has left active service. His peace is short-lived when Felix Leiter, an old friend from the CIA, turns up asking for help.',
    genre: ['Action', 'Adventure', 'Thriller'],
    duration: '2h 43m',
    rating: '7.3',
    year: 2021,
    image: '/images/image32.jpg',
    platform: 'Prime Video'
  },
  {
    id: '33',
    title: 'Venom: Let There Be Carnage',
    description: 'Eddie Brock attempts to reignite his career by interviewing serial killer Cletus Kasady, who becomes the host of the symbiote Carnage.',
    genre: ['Action', 'Adventure', 'Sci-Fi'],
    duration: '1h 37m',
    rating: '5.9',
    year: 2021,
    image: '/images/image33.jpg',
    platform: 'Netflix'
  },
  {
    id: '34',
    title: 'The Matrix Resurrections',
    description: 'Return to the world of two realities: one, everyday life; the other, what lies behind it.',
    genre: ['Action', 'Sci-Fi'],
    duration: '2h 28m',
    rating: '5.7',
    year: 2021,
    image: '/images/image34.jpg',
    platform: 'Prime Video'
  },
  {
    id: '35',
    title: 'Dune: Part Two',
    description: 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.',
    genre: ['Action', 'Adventure', 'Drama'],
    duration: '2h 46m',
    rating: '8.5',
    year: 2024,
    image: '/images/image35.jpg',
    platform: 'Prime Video'
  },
  {
    id: '36',
    title: 'Oppenheimer',
    description: 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
    genre: ['Biography', 'Drama', 'History'],
    duration: '3h',
    rating: '8.3',
    year: 2023,
    image: '/images/image36.jpg',
    platform: 'Netflix'
  },
  {
    id: '37',
    title: 'Barbie',
    description: 'Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land.',
    genre: ['Adventure', 'Comedy', 'Fantasy'],
    duration: '1h 54m',
    rating: '6.9',
    year: 2023,
    image: '/images/image37.jpg',
    platform: 'Prime Video'
  },
  {
    id: '38',
    title: 'John Wick: Chapter 4',
    description: 'John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy.',
    genre: ['Action', 'Crime', 'Thriller'],
    duration: '2h 49m',
    rating: '7.7',
    year: 2023,
    image: '/images/image38.jpg',
    platform: 'Prime Video'
  },
  {
    id: '39',
    title: 'Guardians of the Galaxy Vol. 3',
    description: 'Still reeling from the loss of Gamora, Peter Quill rallies his team to defend the universe and protect one of their own.',
    genre: ['Action', 'Adventure', 'Comedy'],
    duration: '2h 30m',
    rating: '7.9',
    year: 2023,
    image: '/images/image39.jpg',
    platform: 'Hotstar'
  },
  {
    id: '40',
    title: 'The Flash',
    description: 'Barry Allen uses his super speed to change the past, but his attempt to save his family creates a world without super heroes.',
    genre: ['Action', 'Adventure', 'Fantasy'],
    duration: '2h 24m',
    rating: '6.7',
    year: 2023,
    image: '/images/image40.jpg',
    platform: 'Prime Video'
  },
  {
    id: '41',
    title: 'Indiana Jones and the Dial of Destiny',
    description: 'Archaeologist Indiana Jones races against time to retrieve a legendary artifact that can change the course of history.',
    genre: ['Action', 'Adventure'],
    duration: '2h 34m',
    rating: '6.5',
    year: 2023,
    image: '/images/image41.jpg',
    platform: 'Hotstar'
  },
  {
    id: '42',
    title: 'Transformers: Rise of the Beasts',
    description: 'During the \'90s, a new faction of Transformers - the Maximals - join the Autobots as allies in the battle for Earth.',
    genre: ['Action', 'Adventure', 'Sci-Fi'],
    duration: '2h 7m',
    rating: '6.0',
    year: 2023,
    image: '/images/image42.jpg',
    platform: 'Prime Video'
  },
  {
    id: '43',
    title: 'Scream VI',
    description: 'The survivors of the Ghostface killings leave Woodsboro behind and start a fresh chapter in New York City.',
    genre: ['Horror', 'Mystery', 'Thriller'],
    duration: '2h 3m',
    rating: '6.5',
    year: 2023,
    image: '/images/image43.jpg',
    platform: 'Netflix'
  },
  {
    id: '44',
    title: 'Ant-Man and the Wasp: Quantumania',
    description: 'Scott Lang and Hope Van Dyne are dragged into the Quantum Realm, along with Hope\'s parents and Scott\'s daughter Cassie.',
    genre: ['Action', 'Adventure', 'Comedy'],
    duration: '2h 5m',
    rating: '6.1',
    year: 2023,
    image: '/images/image44.jpg',
    platform: 'Hotstar'
  },
  {
    id: '45',
    title: 'Avatar: The Last Airbender',
    description: 'A young boy known as the Avatar must master the four elemental powers to save the world, and fight against an evil Fire Nation.',
    genre: ['Action', 'Adventure', 'Family'],
    duration: '1h',
    rating: '8.7',
    year: 2024,
    image: '/images/image45.jpg',
    platform: 'Netflix'
  }
];

export const heroSlides = [
  {
    id: 'slide1',
    title: 'ICC Champions Trophy',
    image: '/images/cricket.png',
    type: 'sports'
  },
  {
    id: 'slide2',
    title: 'Chhaava',
    image: '/images/trending.png',
    type: 'movies'
  },
  {
    id: 'slide3',
    title: 'BIGG BOSS',
    image: '/images/tvshows.png',
    type: 'tv'
  },
  {
    id: 'slide4',
    title: 'Stranger Things',
    image: '/images/series.png',
    type: 'series'
  }
];

function getRandomSubset(data, count = 15) {
  return [...data].sort(() => Math.random() - 0.5).slice(0, count);
}

export const movieCategories = {
  'Personal Picks for You': getRandomSubset(movieData, 15),
  'Based on Your Watch History': getRandomSubset(movieData, 15),
  'Friends Are Watching': getRandomSubset(movieData, 15),
  'Currently Trending': movieData
    .filter(m => [2024, 2023, 2022].includes(m.year))
    .slice(0, 15),
  'Popular Around You': getRandomSubset(movieData, 15),
  'Action-Packed Adventures': movieData
    .filter(m => m.genre.includes('Action'))
    .slice(0, 15),
  'Laugh Out Loud (Comedy)': movieData
    .filter(m => m.genre.includes('Comedy'))
    .slice(0, 15),
  'Emotional Dramas': movieData
    .filter(m => m.genre.includes('Drama'))
    .slice(0, 15),
  'Gripping Crime Thrillers': movieData
    .filter(m => m.genre.includes('Crime'))
    .slice(0, 15),
  'Fantasy Escapes': movieData
    .filter(m => m.genre.includes('Fantasy'))
    .slice(0, 15),
  'Sci-Fi Journeys': movieData
    .filter(m => m.genre.includes('Sci-Fi'))
    .slice(0, 15),
  'Netflix Originals': movieData
    .filter(m => m.platform === 'Netflix')
    .slice(0, 15),
  'Prime Video Highlights': movieData
    .filter(m => m.platform === 'Prime Video')
    .slice(0, 15),
  'Hotstar Specials': movieData
    .filter(m => m.platform === 'Hotstar')
    .slice(0, 15),
  'Aha Originals': movieData
    .filter(m => m.platform === 'Aha')
    .slice(0, 15)
};


export const allCategories = ['All', 'Action', 'Adventure', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Sports'];

export const predefinedMovies = movieData.map(movie => movie.title);

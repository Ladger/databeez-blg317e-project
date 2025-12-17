const TABLE_SCHEMAS = {
    'Game': { 
        title: 'Game',
        idKey: 'Game_ID', 
        columns: [
            { key: 'Name', label: 'Name' },
            { key: 'Year', label: 'Year' },
            { key: 'Rank', label: 'Rank' },
            { key: 'Publisher_Name', label: 'Publisher' }, 
            { key: 'Platform_Name', label: 'Platform' },
            { key: 'Genre_Name', label: 'Genre' }
        ] 
    },
    'Publisher': { 
        title: 'Publisher',
        idKey: 'Publisher_ID', 
        columns: [
            { key: 'Publisher_Name', label: 'Publisher' }, 
            { key: 'Country', label: 'Country' }, 
            { key: 'Year_Established', label: 'Year Established' }
        ] 
    },
    'Platform': { 
        title: 'Platform',
        idKey: 'Platform_ID', 
        columns: [
            { key: 'Platform_Name', label: 'Platform' }, 
            { key: 'Manufacturer', label: 'Manufacturer' }, 
            { key: 'Release_Year', label: 'Release Year' }
        ] 
    },
    'Genre': { 
        title: 'Genre',
        idKey: 'Genre_ID', 
        columns: [
            { key: 'Genre_Name', label: 'Genre' }, 
            { key: 'Description', label: 'Description' }, 
            { key: 'Example_Game', label: 'Example Game' }
        ] 
    },
    'Sales': { 
        title: 'Sales',
        idKey: 'Sales_ID', 
        columns: [
            { key: 'Game_Name', label: 'Game' }, 
            { key: 'NA_Sales', label: 'NA Sales (M)' }, 
            { key: 'EU_Sales', label: 'EU Sales (M)' }, 
            { key: 'JP_Sales', label: 'JP Sales (M)' }, 
            { key: 'Other_Sales', label: 'Other Sales (M)' }, 
            { key: 'Global_Sales', label: 'Global Sales (M)' }
        ] 
    }
};

const FORM_SCHEMAS = {
    'Game': {
        title: 'Add New Game',
        endpoint: 'add_game',
        fields: [
            { name: 'game_name', label: 'Game Name', type: 'text', required: true },
            { name: 'game_year', label: 'Release Year', type: 'number', placeholder: 'YYYY', min: 1950, max: 2025 },
            
            { type: 'separator', label: 'Associations' },
            { 
                name: 'publisher_id', 
                label: 'Publisher', 
                type: 'search-select', 
                lookupTable: 'Publisher', 
                required: true 
            },
            { 
                name: 'platform_id', 
                label: 'Platform', 
                type: 'search-select', 
                lookupTable: 'Platform', 
                required: true 
            },
            { 
                name: 'genre_id', 
                label: 'Genre', 
                type: 'search-select', 
                lookupTable: 'Genre', 
                required: true 
            },

            { type: 'separator', label: 'Sales Data (Millions)' },
            { name: 'na_sales', label: 'NA Sales', type: 'number', step: '0.01' },
            { name: 'eu_sales', label: 'EU Sales', type: 'number', step: '0.01' },
            { name: 'jp_sales', label: 'JP Sales', type: 'number', step: '0.01' },
            { name: 'other_sales', label: 'Other Sales', type: 'number', step: '0.01' }
        ]
    },
    'Publisher': {
        title: 'Add New Publisher',
        endpoint: 'add_publisher',
        fields: [
            { name: 'publisher_name', label: 'Publisher Name', type: 'text', required: true },
            { name: 'country', label: 'Country', type: 'text' },
            { name: 'year_established', label: 'Year Established', type: 'number', placeholder: 'YYYY' }
        ]
    },
    'Platform': {
        title: 'Add New Platform',
        endpoint: 'add_platform',
        fields: [
            { name: 'platform_name', label: 'Platform Name', type: 'text', required: true },
            { name: 'manufacturer', label: 'Manufacturer', type: 'text' },
            { name: 'release_year', label: 'Release Year', type: 'number', placeholder: 'YYYY' }
        ]
    },
    'Genre': {
        title: 'Add New Genre',
        endpoint: 'add_genre',
        fields: [
            { name: 'genre_name', label: 'Genre Name', type: 'text', required: true },
            { name: 'description', label: 'Description', type: 'text' },
            { name: 'example_game', label: 'Example Game', type: 'text' }
        ]
    }
};
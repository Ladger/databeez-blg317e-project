const TABLE_SCHEMAS = {
    'table-1': { 
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
    'table-2': { 
        title: 'Publisher',
        idKey: 'Publisher_ID', 
        columns: [
            { key: 'Publisher_Name', label: 'Publisher' }, 
            { key: 'Country', label: 'Country' }, 
            { key: 'Year_Established', label: 'Year Established' }
        ] 
    },
    'table-3': { 
        title: 'Platform',
        idKey: 'Platform_ID', 
        columns: [
            { key: 'Platform_Name', label: 'Platform' }, 
            { key: 'Manufacturer', label: 'Manufacturer' }, 
            { key: 'Release_Year', label: 'Release Year' }
        ] 
    },
    'table-4': { 
        title: 'Genre',
        idKey: 'Genre_ID', 
        columns: [
            { key: 'Genre_Name', label: 'Genre' }, 
            { key: 'Description', label: 'Description' }, 
            { key: 'Example_Game', label: 'Example Game' }
        ] 
    },
    'table-5': { 
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
    'table-1': {
        title: 'Add New Game',
        endpoint: 'add_game',
        fields: [
            // Oyun Temel Bilgileri
            { name: 'game_name', label: 'Game Name', type: 'text', required: true },
            { name: 'game_year', label: 'Release Year', type: 'number', placeholder: 'YYYY', min: 1950, max: 2025 },
            { name: 'game_rank', label: 'Rank', type: 'number', required: true },
            
            // Satış Bilgileri (Oyun formuna dahil edildi)
            { type: 'separator', label: 'Sales Data (Millions)' },
            { name: 'na_sales', label: 'NA Sales', type: 'number', step: '0.01' },
            { name: 'eu_sales', label: 'EU Sales', type: 'number', step: '0.01' },
            { name: 'jp_sales', label: 'JP Sales', type: 'number', step: '0.01' },
            { name: 'other_sales', label: 'Other Sales', type: 'number', step: '0.01' },
            { name: 'global_sales', label: 'Global Sales', type: 'number', step: '0.01' },

            // İlişkiler
            { type: 'separator', label: 'Foreign Keys' },
            { name: 'publisher_id', label: 'Publisher ID', type: 'number', required: true },
            { name: 'platform_id', label: 'Platform ID', type: 'number', required: true },
            { name: 'genre_id', label: 'Genre ID', type: 'number', required: true }
        ]
    },
    'table-2': {
        title: 'Add New Publisher',
        endpoint: 'add_publisher',
        fields: [
            { name: 'publisher_name', label: 'Publisher Name', type: 'text', required: true },
            { name: 'country', label: 'Country', type: 'text' },
            { name: 'year_established', label: 'Year Established', type: 'number', placeholder: 'YYYY' }
        ]
    },
    'table-3': {
        title: 'Add New Platform',
        endpoint: 'add_platform',
        fields: [
            { name: 'platform_name', label: 'Platform Name', type: 'text', required: true },
            { name: 'manufacturer', label: 'Manufacturer', type: 'text' },
            { name: 'release_year', label: 'Release Year', type: 'number', placeholder: 'YYYY' }
        ]
    },
    'table-4': {
        title: 'Add New Genre',
        endpoint: 'add_genre',
        fields: [
            { name: 'genre_name', label: 'Genre Name', type: 'text', required: true },
            { name: 'description', label: 'Description', type: 'text' }
        ]
    }
};
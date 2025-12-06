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
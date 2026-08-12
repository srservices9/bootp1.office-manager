flowchart LR
    Browser["User's browser (LAN)"] -->|HTTP| Flask["Flask app"]
    Flask -->|file metadata| DB[("SQLite database")]
    Flask -->|file bytes| Disk[("uploads/ folder")]

erDiagram
    FOLDER ||--o{ FOLDER : "contains (subfolders)"
    FOLDER ||--o{ FILE : "holds"
    FOLDER {
        int id
        string name
        int parent_id
    }
    FILE {
        int id
        string filename
        string stored_name
        int size_bytes
        string mime_type
        datetime uploaded_at
    }

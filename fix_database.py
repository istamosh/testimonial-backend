#!/usr/bin/env python3
"""
Script to manually fix the database schema for testimonials
"""
import sqlite3
import os

# Path to the database
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'users.db')

def fix_testimonial_schema():
    """Fix the testimonial table schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(testimonial)")
        columns = cursor.fetchall()
        print("Current columns:")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        
        # Get existing column names
        existing_columns = [col[1] for col in columns]
        
        # Define required columns for new schema
        required_columns = {
            'first_name': 'VARCHAR(60)',
            'last_name': 'VARCHAR(60)', 
            'role_company': 'VARCHAR(120)',
            'testimonial': 'TEXT',
            'censor_first_name': 'BOOLEAN DEFAULT 0',
            'censor_last_name': 'BOOLEAN DEFAULT 0',
            'consent_given': 'BOOLEAN DEFAULT 0'
        }
        
        # Add missing columns
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                print(f"Adding column: {col_name}")
                if 'DEFAULT' in col_type:
                    cursor.execute(f"ALTER TABLE testimonial ADD COLUMN {col_name} {col_type}")
                else:
                    # For non-nullable columns without default, add as nullable first
                    cursor.execute(f"ALTER TABLE testimonial ADD COLUMN {col_name} {col_type}")
        
        # Migrate existing data if nameOrEmail and linkedin_url exist
        if 'nameOrEmail' in existing_columns:
            print("Migrating existing data...")
            # Split nameOrEmail into first_name and last_name (simple approach)
            cursor.execute("""
                UPDATE testimonial 
                SET first_name = CASE 
                    WHEN instr(nameOrEmail, ' ') > 0 
                    THEN substr(nameOrEmail, 1, instr(nameOrEmail, ' ') - 1)
                    ELSE nameOrEmail
                END,
                last_name = CASE 
                    WHEN instr(nameOrEmail, ' ') > 0 
                    THEN substr(nameOrEmail, instr(nameOrEmail, ' ') + 1)
                    ELSE ''
                END,
                consent_given = 1
                WHERE first_name IS NULL OR first_name = ''
            """)
            
            # Set default values for boolean fields
            cursor.execute("""
                UPDATE testimonial 
                SET censor_first_name = 0, 
                    censor_last_name = 0
                WHERE censor_first_name IS NULL
            """)
        
        conn.commit()
        print("Database schema updated successfully!")
        
        # Show final schema
        cursor.execute("PRAGMA table_info(testimonial)")
        columns = cursor.fetchall()
        print("\nFinal columns:")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_testimonial_schema()

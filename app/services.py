from app.database import get_connection

def list_plans():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type FROM plans")
    planos = cursor.fetchall()
    conn.close()
    
    return [{"id": p[0], "type": p[1]} for p in planos]

def create_user(user_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (address, email, cpf, plan_id, status, status_reason)
            VALUES (?, ?, ?, ?, 'active', NULL)
        """, (
            user_data["address"],
            user_data["email"],
            user_data["cpf"],
            user_data["plan_id"]
        ))
        conn.commit()
        novo_id = cursor.lastrowid
        return search_user(novo_id)
    finally:
        conn.close()

def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.id, u.address, u.email, u.cpf, u.plan_id, p.type
        FROM users u
        JOIN plans p ON u.plan_id = p.id
    """)
    usuarios = cursor.fetchall()
    conn.close()
    
    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u[0],
            "address": u[1],
            "email": u[2],
            "cpf": u[3],
            "plan_id": u[4],
            "plan_type": u[5]
        })
    return resultado

def search_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.id, u.address, u.email, u.cpf, u.plan_id, p.type, u.status, u.status_reason
            FROM users u
            JOIN plans p ON u.plan_id = p.id
            WHERE u.id = ?
        """, (user_id,))
        u = cursor.fetchone()
        if u is None:
            return None
        return {
            "id": u[0], "address": u[1], "email": u[2], "cpf": u[3],
            "plan_id": u[4], "plan_type": u[5], "status": u[6], "status_reason": u[7]
        }
    finally:
        conn.close()

def update_user(user_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Se for um update fixo:
        cursor.execute("""
            UPDATE users
            SET address = ?, email = ?, cpf = ?, plan_id = ?
            WHERE id = ?
        """, (data.get("address"), data.get("email"), data.get("cpf"), data.get("plan_id"), user_id))
        
        conn.commit()
        return search_user(user_id)
    finally:
        conn.close()

def patch_user(user_id: int, data: dict):
    if not data:
        return search_user(user_id) # Se nenhum campo foi enviado, retorna o usuário atual

    conn = get_connection()
    cursor = conn.cursor()
    
    # Monta as cláusulas SET dinamicamente (ex: "address = ?, email = ?")
    fields = [f"{key} = ?" for key in data.keys()]
    values = list(data.values())
    values.append(user_id) # Para o WHERE id = ?
    
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    
    return search_user(user_id)

def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
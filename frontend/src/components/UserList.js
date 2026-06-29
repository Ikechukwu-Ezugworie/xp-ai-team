import React from 'react';

function UserList({ members }) {
  return (
    <div className="user-list">
      <h3>Members ({members.length})</h3>
      <ul>
        {members.map((m) => (
          <li key={m.user_id} className="user-item">
            <span className="user-dot" />
            {m.username}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;

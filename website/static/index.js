function deleteNote(note_id){
    fetch('/delete-note', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ note_id: note_id }),
    }).then((_res) => {
        window.location.href = '/study-tools';
    });
}


document.querySelectorAll('.deleteNoteButton').forEach(button => {
    button.addEventListener('click', function() {
        // get the note ID from the button or its parent
        var noteId = this.parentNode.getAttribute('data-note-id');
        deleteNote(noteId);
    });
});

document.getElementById('addNoteBtn').addEventListener('click', function() {
    document.getElementById('noteForm').submit();
});

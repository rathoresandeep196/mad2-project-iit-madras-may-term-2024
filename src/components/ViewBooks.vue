<template>
    <div>
      <h1>All Books</h1>
      <div class="books-container">
        <div v-for="book in books" :key="book.id" class="book">
          <h3>{{ book.title }}</h3>
          <p>{{ book.description }}</p>
          <div class="button-group">
            <!-- <a :href="'/assets/' + book.id">View</a> -->
            <!-- <a :href="getPdfPath(book.id)">View</a> -->
             <div>
                <button @click="downloadPdf(book.id)">view</button>
             </div>
            <button @click="editBook(book.id)">Edit</button>
            <button @click="confirmDelete(book.id)">Delete</button>
          </div>
        </div>
      </div>
      <div v-if="showConfirmModal" class="confirm-modal">
        <p>Are you sure you want to delete this book?</p>
        <div>
          <button @click="deleteBook">Delete</button>
          <button @click="cancelDelete">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ViewBooks',
    data() {
      return {
        books: [],
        showConfirmModal: false,
        bookToDelete: null
      };
    },
    mounted() {
      this.fetchBooks();
    },
    methods: {
      fetchBooks() {
        this.$axios
          .get('/books', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
              // ContentType : `multipart/form-data`,
            },
          })
          .then(response => {
            this.books = response.data.books;
          })
          .catch(error => {
            console.error('Error fetching books:', error);
          });
      },
      downloadPdf(id) {
        const url =`http://localhost:5000/assets/${id}.pdf`;
        window.open(url, '_blank');
      },
      editBook(id) {
        this.$router.push(`/edit-book/${id}`);
      },
      confirmDelete(id) {
        this.showConfirmModal = true;
        this.bookToDelete = id;
      },
      deleteBook() {
        this.$axios
          .delete(`/book/${this.bookToDelete}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
              // ContentType : `multipart/form-data`,
            },
          })
          .then(() => {
            this.fetchBooks(); // Refresh the book list
            this.showConfirmModal = false;
            this.bookToDelete = null;
          })
          .catch(error => {
            console.error('Error deleting book:', error);
          });
      },
      cancelDelete() {
        this.showConfirmModal = false;
        this.bookToDelete = null;
      }
    }
  };
  </script>
  
  <style scoped>
  .books-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .book {
    border: 1px solid #ccc;
    padding: 10px;
    width: calc(33.33% - 20px);
    box-sizing: border-box;
  }
  
  .book h3 {
    margin-bottom: 5px;
  }
  
  .button-group {
    margin-top: 10px;
  }
  
  .confirm-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .confirm-modal p {
    background-color: white;
    padding: 20px;
    border-radius: 5px;
    text-align: center;
  }
  
  .confirm-modal div {
    margin-top: 10px;
  }
  
  .confirm-modal button {
    padding: 10px 20px;
    margin: 0 10px;
    cursor: pointer;
  }
  </style>
  
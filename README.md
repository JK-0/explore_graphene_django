# explore_graphene_django

### admin link
`http://ec2-18-237-131-39.us-west-2.compute.amazonaws.com/admin/`

### graph link
`http://ec2-18-237-131-39.us-west-2.compute.amazonaws.com/graphql`

### Graphql Query's

- Show list of all movies present in the database.
```
query{
  	allMovie {
      id
      title
      releaseDate
      overview
      genre {
        name
      }
    }
}
```

- Show detailed data of a particular movie given id as the argument.

```
query{
	movieById(id:10){
    title
    releaseDate
    overview
    genre{
      name
    }
  }
}
```

- create play list of movie

```
mutation{
  createPlaylist(name:"my watch list", owner:1, movie:[10, 11]){
    playList{
      name
      movie{
        id
        title
      }
    }
  }
}
```

- update play list details
```
mutation{
  updatePlaylist(id:1, movie: [15, 16]){
    playList{
      name
      id
      movie{
        title
        id
      }
    }
  }
}
```

- add movie to play list
```
mutation{
	addMovieToPlaylist(id:1, movie:25){
    playList{
      name
      id
      movie{
        id
        title
      }
    }
  }
}
```

- suggest movie based on play list (suggestion logic might be different based on requirement)

```
{
  suggestMovie(id: 1) {
    title
    id
    genre {
      id
      name
    }
  }
}
```
function (doc) {
    xmax = 149.263643
  xmin = 148.995922
  ymax = -35.147699
  ymin = -35.48026
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Canberra"){
      emit(doc._id,doc)
    }
  }
}

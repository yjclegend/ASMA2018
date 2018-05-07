function (doc) {
  if(doc.placename=="Hobart"){
    emit(doc.text,doc.coordinates)
  }
}

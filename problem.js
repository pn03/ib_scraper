let mongoose = require('mongoose')
let validator = require('validator')

let problemSchema = new mongoose.Schema({
  question_slug: {
    type: String,
    required: true,
    unique: true,
  },
  is_archived:Boolean,
  question_title:String,
  topics:[String],
  hints:[String],
  question_html:String,
  question_link:String,
  voted_solution_html:[String],
  voted_solution_link:[String],
  voted_solution_title:[String],
  my_solution_html:String,
  backend_question_id:Number,
  frontend_question_id:Number,
  is_premium:Boolean,
  difficulty:Number,
  has_images:Boolean,
  images_paths:[String],
  createdOn:Date,
  updatedOn:Date
})

problemSchema.pre('save', function(next) {
  // get the current date
  var currentDate = new Date();

  // change the updated_at field to current date
  this.updatedOn = currentDate;

  // if created_at doesn't exist, add to that field
  if (!this.createdOn)
    this.createdOn = currentDate;

  next();
});

problemSchema.methods.isPremium = function(){
  return this.is_premium;
}

problemSchema.methods.getDifficulty = function(){
  return this.difficulty;
}

problemSchema.methods.getQuestionSlug = function(){
  return this.question_slug;
}

module.exports = mongoose.model('Problem', problemSchema)
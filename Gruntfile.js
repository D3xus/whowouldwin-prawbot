/* This is a grunt file. It sets up lots of automated tasks, so we can type a couple words and do a bunch of things. */

module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt); // npm install --save-dev load-grunt-tasks

  grunt.initConfig({
    sass: {
      reddit: {
        options: {
          // style: 'expanded', // makes the output CSS code human readable.
          style: 'compressed', // removes the line breaks and spaces to put the code all on one line.
          noCache: true
        },
        files: {
          'reddit/reddit.css': 'src/sass_reddit/main.scss'
        }
      },
      site: {
        options: {
          // style: 'expanded', // makes the output CSS code human readable.
          style: 'compressed', // removes the line breaks and spaces to put the code all on one line.
          noCache: true
        },
        files: {
          'static/flairbot.css': 'src/sass_site/main.scss'
        }
      }
    },
    sync: {
      scripts: {
        files: [
          { 
            cwd: 'src',
            src: [
              'img/**/*',
              '!node_modules/**/*'
            ], 
            dest: 'static' 
          },
          { 
            cwd: 'src',
            src: [
              '**/*.html',
            ], 
            dest: 'templates' 
          }
        ]
      }
    },
    watch: {
      html: {
        files: ['src/**/*.html','src/!node_modules/**/*'],
        tasks: ['sync']
      },
      img: {
        files: ['src/img/**/*'],
        tasks: ['sync']
      },
      scss: {
        files: ['src/sass_site/**/*'],
        tasks: ['sass']
      },
      grunt: {
        files: 'Gruntfile.js',
        tasks: ['build']
      }
    }
  });
  
  // > grunt build_reddit - compiles project for reddit's stylesheet
  grunt.registerTask('build', ['build_reddit', 'build_site']);
  // > grunt build_reddit - compiles project for reddit's stylesheet
  grunt.registerTask('build_reddit', ['sass:reddit']);
  // > grunt build_site  - compiles project for the reddit chooser
  grunt.registerTask('build_site', ['sass:site', 'sync']);    
  // > grunt start  - compiles project and re-builds project when files change
  grunt.registerTask('start', ['build', 'watch']);
  // > grunt        - compiles project (defining default task)
  grunt.registerTask('default', ['build']);
}
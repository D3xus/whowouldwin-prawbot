/* This is a grunt file. It sets up lots of automated tasks, so we can type a couple words and do a bunch of things. */

module.exports = function(grunt) {

  require('load-grunt-tasks')(grunt); // npm install --save-dev load-grunt-tasks

  grunt.initConfig({
    sass: {
      dist: {
        options: {
          // style: 'expanded', // makes the output CSS code human readable. 
          style: 'compressed', // removes the line breaks and spaces to put the code all on one line.
          noCache: true
        },
        files: {
            'static/flairbot.css' : 'src/sass/main.scss'
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
        files: ['src/sass/**/*'],
        tasks: ['sass']
      },
      grunt: {
        files: 'Gruntfile.js',
        tasks: ['build']
      }
    },
    connect: {
      server: {
        options: {
          port: 9000,
          base: 'dist',
          middleware: function(connect, options, middlewares) {
            middlewares.unshift(function(req, res, next) {
              res.setHeader('Access-Control-Allow-Origin', '*');
              next();
            });
            return middlewares;
          }
        }
      }
    }
  });

  // > grunt deploy - compiles project and sends to ftp
  grunt.registerTask('deploy', ['build', 'ftp-deploy']);                
  // > grunt build  - compiles project
  grunt.registerTask('build', ['sass', 'sync']);    
  // > grunt start  - compiles project, runs localhost server at http://localhost:9000 and re-builds project when files change
  grunt.registerTask('start', ['build', 'connect', 'watch']);
  // > grunt        - compiles project (defining default task)
  grunt.registerTask('default', ['build']);
}
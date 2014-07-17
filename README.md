gitime
====

Keep track of your billable hours along with your commits. Gitime lets you build an invoice with your tasks and hours worked from your commit messages.

Simple Usage
----

Set your hourly rate.

```sh
$ gitime settings -r 50
```

Start a new invoice.

```sh
$ gitime invoice -n "Awesome Secret Project"
```

Time how long you've been working.

```sh
$ gitime timer start
```

Make a commit as you would normally, but on the commit step, use `gitime` instead of `git`.

```sh
$ git add .
$ gitime commit -m "Added a really cool thing"
$ git push
```

Look at your invoice.

```sh
$ gitime status
On invoice Awesome Secret Project
Total time worked: 2 hours
Total charges:     $100.00
Charges:
2 hours            Added a really cool thing
```

When it's time to bill, export your invoice to a spreadsheet.

```sh
$ gitime export
```
=======================================
 Django Bitbucket & Trello Integration
=======================================

Goals
=====

The main goal is to develop a standalone application that can seamlessly integrate Bitbucket and Trello. It can be further divided into smaller goals which are the following:

- Define a staging branch that can trigger a specific Trello card to move to another specified Trello list (e.g. Testing)
- Define a production branch that can trigger a specific Trello card to move to another specified Trello list (e.g. Done)
- Any Trello card mentions following pattern #<card_number> in a commit message shall be added to the corresponding card as a comment
- Keep application architecture flexible for easier extensibility in the future
- Easy initial setup, such as API authorization, application settings

Overview
========

Here’s some history background. We use Bitbucket as a code repository and we have recently switched to Trello as part of Agile methodology. Basically our team consists of developers and a QA team (testers).

Our development process works the following way. The project owner lays down a number of Trello cards in, let’s say, To Do list that are primary goals of our project that we have to complete. Developers pick them up one by one and move them onto Doing list, create a branch and start working on it. Once we complete a task, we push it to Bitbucket repository, merge it to the staging branch and manually move a corresponding Trello card from Doing list onto Testing list.

That’s when testers come into play. They test a feature and when it has no issues they move it from Testing onto Done. Upon that we, developers, get a notification from Trello and then we go to Bitbucket and create new pull request, then merge it to the production branch.

It’s obvious that moving cards here and there is much of a hassle and takes up a lot of our time that we could spend on actual development. There were other online Kanban boards that had integration with Bitbucket of course, but we really like Trello due to its simplicity and user-friendliness. We couldn’t find any free solution on Internet either that would integrate Trello and Bitbucket. Then I decided to create it on my own.

Prerequisites
=============

I assume that you already have an app server, Bitbucket repository for your project and a Trello board. In order to use this application you need to get some stuff in your hand first. First of all, you need to get a token and an app key from here. Secondly, make sure you get an ID of the lists you are about to use; you may get them through their API by passing a board ID.

Once you acquire a token and an app key, think of a flow that you will have, meaning properly naming branches and Trello lists. As for us, our staging branch is called master, which is the latest but unstable, and our production branch is called production, which might be the latest but it’s stable. Our Trello list are as follows: To Do -> Doing -> Testing -> Done.



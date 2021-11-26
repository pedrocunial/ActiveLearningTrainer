# PFE-2018-IBM
![CircleCI token](https://img.shields.io/circleci/token/43d13c1ca40cf63b620286dc9419263627935cc4/project/github/Insper/PFE-2018-IBM/master.svg)

Repositório para o desenvolvimento do Projeto Final de engenharia para a IBM.

O projeto consiste em uma ferramenta de rotulagem para os classificadores NLC e VR da IBM Cloud.

## Estrutura do projeto

Esse repositório contém o WebApp e a Business Layer da ferramenta, os dois serviços da solução, nas pastas `frontend` e `backend`, respectivamente.

## Setup

O guia de utilização do projeto está descrito em cada serviço separadamente.

## Mantenedores

- Gustavo Efeiche
- Lucas Astur
- Marcelo Andrade
- Pedro Cunial

## Guia de desenvolvimento

Os serviços _frontend_ e _backend_ são desenvolvidos em _branches_ separados, e ao final de cada release do projeto, anexadas ao branch `master`.

Quando for contribuir para um projeto específico, use a seguinte convenção de nomes para criação de _branches_:

- bug    - consertar uma _issue_
- feat   - nova _feature_
- hotfix - uma breve mudança no código
- junk   - experimentos (nunca vão ser anexadas)

O nome do _branch_ deve ser o nome de um dos itens acima, seguido do serviço em que está trabalhando (`frontend` ou `backend`) e, por fim, uma breve descrição do que está fazendo. 

Exemplos:

- bug/frontend/image-not-showing
- hotfix/frontend/remove-comments
- bug/backend/nlc-breaks-empty-list
- feat/backend/vr-classifier
- feat/frontend/manage-projects

Ao final da contribuição, crie um _Pull Request_ para o _branch_ do respectivo serviço. Esse _Pull Request_ deve ser aceito no mínimo pelo(s) membro(s) que está(ão) trabalhando no mesmo serviço durante a _sprint_. Após o _Pull Request_ ser aceito, remova o _branch_ criado, deletando-o na seção [_branches_](https://github.com/Insper/PFE-2018-IBM/branches) e na cópia local do repositório, utilizando `$ git branch -D <branch>`.

Ao final de uma _sprint_ ou _release_ da ferramenta, os dois branches `frontend` e `backend` farão um _Pull Request_ para o branch `master` com as mudanças da _sprint_. Esses dois _Pull Requests_ devem ser revisados e aceitos por todos os membros do grupo.

Caso seja feita uma nova _feature_ que envolva uma mudança de protocolo de comunicação entre o `frontend` e o `backend`, liste essa nova comunicação na descrição do _Pull Request_. O mesmo só deve ser aceito quando houver um _Pull Request_ condizente com a _feature_ no outro serviço também.

Nesse momento, será criada uma tag para o projeto, marcando uma nova release.

### Trabalhando no _frontend_ e _backend_ ao mesmo tempo
Para facilitar o trabalho nos serviços de `frontend` e `backend` na mesma máquina, deve ser criada, localmente, uma nova _worktree_ para o repositório. [Este link](https://git-scm.com/docs/git-worktree) explica o conceito de _worktrees_. Esta técnica permite ao programador trabalhar em dois _branches_ ao mesmo tempo, evitando ter de clonar duas vezes o repositório.

Estando na raíz do repositório, faça _checkout_ no _branch_ `frontend` utilizando `$ git checkout frontend`. Em seguida, crie a nova _worktree_ com `$ git worktree add ../pfe_frontend`. Será criada uma nova pasta, com nome `pfe_frontend/`, do "lado de fora" do repositório. Esta nova pasta representa a nova _worktree_. Ela é uma cópia exata do repositório original, porém está conectada a ele. Nesta nova pasta é possível trabalhar como se estivesse no reposítório original, trocando de _branches_, editando e _commitando_ arquivos, etc. Mudanças realizadas na nova pasta serão refletidas na pasta original. Portanto, para organização da equipe, a nova pasta servirá para trabalhos no _branch_ `frontend`, enquanto a pasta contendo a cópia original será utilizada para trabalhos no _branch_ `backend`. Recomenda-se renomear a pasta com a cópia original do repositório para `pfe_backend`, para fácil identificação da _worktree_ a ser utilizada.

##### Exemplo de workflow com duas _worktrees_:

Modificando o _frontend_

```sh
$ cd pfe_frontend
$ git checkout frontend
$ git pull origin frontend
$ git checkout -b feat/frontend/example-feature
...modificações no frontend...
$ git add <modified_files>
$ git commit -m "..."
$ git push -u origin feat/frontend/example-feature
...Pull Request deste novo branch para o branch remoto frontend...
```

Modificando o _backend_

```sh
$ cd pfe_backend
$ git checkout backend
$ git pull origin backend
$ git checkout -b feat/backend/example-feature
...modificações no backend...
$ git add <modified_files>
$ git commit -m "..."
$ git push -u origin feat/backend/example-feature
...Pull Request deste novo branch para o branch remoto backend...
```

#ifndef ALUNOS_H
#define ALUNOS_H

typedef struct alunos
{
    char email[100];
    char nome[100];
    int idade;
    float nota;
} Aluno;

void lancarNota();
void cadastrarAluno();
void listarAlunos();
void atualizarAluno();
void excluirAluno();

#endif
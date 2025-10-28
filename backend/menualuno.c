#include <stdio.h>
#include <string.h>
#include "../routes/menualuno.h"
#include "../routes/menuprof.h" 

#define ARQ_ALUNOS "database/alunos.txt"

void verNota() {
    char email[100];
    float nota;
    char emailBusca[100];
    int encontrado = 0;

    printf("Digite seu email para ver a nota: ");
    scanf("%99s", emailBusca);

    FILE *arquivo = fopen(ARQ_ALUNOS, "r");
    if (!arquivo) {
        printf("Nenhuma nota registrada ainda.\n");
        return;
    }

    while (fscanf(arquivo, "%99[^;];%f\n", email, &nota) == 2) {
        if (strcmp(email, emailBusca) == 0) {
            printf("Sua nota é: %.2f\n", nota);
            encontrado = 1;
            break;
        }
    }
    fclose(arquivo);

    if (!encontrado)
        printf("Nota não encontrada para o email informado.\n");
}